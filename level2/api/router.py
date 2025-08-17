



from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os, redis
from rq import Queue
from ..dto import AnalysisConfig
from ..repository.weaviate_repo import WeaviateRepository
from ..pipeline.orchestrator import Level2Orchestrator
import weaviate

router = APIRouter(prefix="/level2", tags=["level2"])

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



