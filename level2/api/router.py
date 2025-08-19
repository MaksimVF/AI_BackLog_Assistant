




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



