




from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List
import os, redis
from rq import Queue
from ..dto import AnalysisConfig, Task
from ..repository.weaviate_repo import WeaviateRepository
from ..pipeline.orchestrator import Level2Orchestrator
from ..api.dto import StrategicAnalysisRequest, StrategicAnalysisResult
from ..db.models import StrategicAnalysisSnapshot
from ..db.repo import StrategicRepo
from ..strategy.orchestrator import StrategicOrchestrator
from ..integrations.jira_client import JiraClient, JiraConfig
from ..integrations.trello_client import TrelloClient, TrelloConfig
from ..integrations.sync_service import SyncService
from ..api.integration_dto import (
    JiraConfig as JiraConfigDTO,
    TrelloConfig as TrelloConfigDTO,
    SyncRequest,
    SyncResult,
    IntegrationStatus,
    CreateExternalTaskRequest,
    CreateExternalTaskResponse
)
# from ..teamwork.api.router import router as teamwork_router
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_async_session
from ..visualization.visualization_aggregator import VisualizationAggregator
import weaviate


router = APIRouter(prefix="/level2", tags=["level2"])

# Include teamwork router
# router.include_router(teamwork_router, prefix="/teamwork", tags=["Teamwork"])


class AnalyzeRequest(BaseModel):
    project_id: str
    config: Optional[AnalysisConfig] = None
    async_mode: bool = True

@router.post("/analyze")
def analyze(req: AnalyzeRequest):
    cfg = req.config or AnalysisConfig()
    if req.async_mode:
        r = redis.from_url(os.environ["REDIS_URL"])
        q = Queue("level2", connection=r)
        job = q.enqueue("ai_backlog_assistant.level2.pipeline.worker.run_analysis",
                        req.project_id, cfg.model_dump())
        return {"job_id": job.get_id(), "status": "queued"}
    else:

        # Mock client for testing - replace with actual Weaviate client in production
        client = None

        repo = WeaviateRepository(client)
        orch = Level2Orchestrator(repo)
        res = orch.analyze_project(req.project_id, cfg)
        return res.model_dump()

@router.get("/job/{job_id}")
def job_status(job_id: str):
    r = redis.from_url(os.environ["REDIS_URL"])
    from rq.job import Job
    job = Job.fetch(job_id, connection=r)
    return {"status": job.get_status(), "result": job.result}

@router.post("/strategic/analyze", response_model=List[StrategicAnalysisResult])
async def analyze_strategic(req: StrategicAnalysisRequest, session: AsyncSession = Depends(get_async_session)):
    repo = StrategicRepo(session)
    orch = StrategicOrchestrator()

    # заглушка — в реальности fetch задачи из БД
    tasks = [Task(id="T1", title="Demo task", project_id=req.project_id, created_at=datetime.now(), metadata={"goals":"increase retention","value_per_day":"200","expected_gain":"5000","cost":"1000"})]

    cfg = AnalysisConfig(**(req.config or {}))
    results = await orch.run(tasks, cfg, req.methods)

    saved = []
    for r in results:
        snap = StrategicAnalysisSnapshot(id=None,
            project_id=req.project_id,
            task_id=r["task_id"],
            method=r["method"],
            score=r["score"],
            labels=r["labels"],
            details=r["details"],
            config=req.config
        )
        s = await repo.save_snapshot(snap)
        saved.append(r)
    return saved

@router.get("/strategic/snapshots/{project_id}")
async def get_snapshots(project_id: str, task_id: str = None, session: AsyncSession = Depends(get_async_session)):
    repo = StrategicRepo(session)
    snaps = await repo.get_snapshots(project_id, task_id)
    return snaps

class VisualizationRequest(BaseModel):
    tasks: List[dict]
    output_format: str = "plotly"  # or "static"

@router.post("/visualize", response_class=HTMLResponse)
async def visualize_data(req: VisualizationRequest):
    """
    Generate visualizations from task data.
    Returns HTML with embedded Plotly visualizations.
    """
    try:
        viz = VisualizationAggregator()
        results = viz.run(req.tasks, output_format=req.output_format)

        if req.output_format == "static":
            # Return JSON with static image data
            return JSONResponse(content={
                "status": "success",
                "visualizations": results
            })

        # Return HTML with interactive visualizations
        html_content = viz.to_html(results)
        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/visualize/static", response_class=JSONResponse)
async def visualize_static(req: VisualizationRequest):
    """
    Generate static visualizations (PNG images).
    """
    try:
        viz = VisualizationAggregator()
        results = viz.run(req.tasks, output_format="static")
        return JSONResponse(content={
            "status": "success",
            "visualizations": results
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Integration Endpoints ---

@router.post("/integrations/sync", response_model=SyncResult)
async def sync_with_external_service(
    req: SyncRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Sync tasks with external services (Jira, Trello).
    """
    try:
        sync_service = SyncService()

        if req.service.lower() == "jira":
            result = await sync_service.sync_with_jira(session)
        elif req.service.lower() == "trello":
            result = await sync_service.sync_with_trello(session)
        else:
            raise HTTPException(status_code=400, detail="Unsupported service")

        return SyncResult(
            status=result["status"],
            service=req.service,
            synced_tasks=result.get("synced", 0),
            message=result.get("message")
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/integrations/jira/create", response_model=CreateExternalTaskResponse)
async def create_jira_task(
    req: CreateExternalTaskRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a task in Jira.
    """
    try:
        # Get the local task
        result = await session.execute(
            select(Task).where(Task.id == req.task_id)
        )
        task = result.scalars().first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        sync_service = SyncService()
        jira_issue = await sync_service.create_jira_task(task, session)

        return CreateExternalTaskResponse(
            status="success",
            external_id=jira_issue.key,
            service="jira",
            message="Task created successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/integrations/trello/create", response_model=CreateExternalTaskResponse)
async def create_trello_task(
    req: CreateExternalTaskRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a task in Trello.
    """
    try:
        # Get the local task
        result = await session.execute(
            select(Task).where(Task.id == req.task_id)
        )
        task = result.scalars().first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        sync_service = SyncService()
        trello_card = await sync_service.create_trello_task(task, session)

        return CreateExternalTaskResponse(
            status="success",
            external_id=trello_card.id,
            service="trello",
            message="Task created successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/integrations/status", response_model=List[IntegrationStatus])
async def get_integration_status():
    """
    Get status of all integration services.
    """
    # This would check connection status in a real implementation
    from datetime import timedelta
    return [
        IntegrationStatus(
            service="jira",
            connected=True,
            last_sync=datetime.utcnow(),
            next_sync=datetime.utcnow() + timedelta(hours=1),
            tasks_synced=42
        ),
        IntegrationStatus(
            service="trello",
            connected=True,
            last_sync=datetime.utcnow(),
            next_sync=datetime.utcnow() + timedelta(hours=1),
            tasks_synced=18
        )
    ]

@router.post("/integrations/config/jira", response_model=Dict)
async def configure_jira(config: JiraConfigDTO):
    """
    Configure Jira integration.
    """
    # In a real implementation, this would save the config
    return {"status": "success", "message": "Jira configuration saved"}

@router.post("/integrations/config/trello", response_model=Dict)
async def configure_trello(config: TrelloConfigDTO):
    """
    Configure Trello integration.
    """
    # In a real implementation, this would save the config
    return {"status": "success", "message": "Trello configuration saved"}



