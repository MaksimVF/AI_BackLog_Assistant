
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ...teamwork.dto import VoteRequest, VoteResult, VotingConfig, ConflictConfig, StakeholderAlignmentConfig
from ...teamwork.orchestrator import TeamworkOrchestrator
from ...db.repo_teamwork import TeamworkRepo
from ...db.session import get_async_session

router = APIRouter(prefix="/teamwork", tags=["Teamwork"])

@router.post("/vote", response_model=VoteResult)
async def vote_endpoint(req: VoteRequest, session: AsyncSession = Depends(get_async_session)):
    orch = TeamworkOrchestrator()
    repo = TeamworkRepo(session)
    cfg = VotingConfig()
    result, internals = orch.run_voting(req, cfg)
    await repo.save_voting(req.project_id, req.task_id, [v.dict() for v in req.votes], result.dict())
    return result

@router.post("/conflict")
async def conflict_endpoint(req: VoteRequest, session: AsyncSession = Depends(get_async_session)):
    orch = TeamworkOrchestrator()
    repo = TeamworkRepo(session)
    cfg = ConflictConfig()
    severity, details = orch.analyze_conflict(req, cfg)
    await repo.save_conflict(req.votes[0].voter_id if req.votes else None, req.task_id, details, severity)
    return {"severity": severity, "details": details}

@router.post("/alignment")
async def alignment_endpoint(task_payload: dict, session: AsyncSession = Depends(get_async_session)):
    """
    task_payload: {"project_id": "...", "task": {...}, "project_stakeholders": {...}}
    """
    orch = TeamworkOrchestrator()
    repo = TeamworkRepo(session)
    task_dict = task_payload.get("task", {})
    from level2.dto import Task as CoreTask
    t = CoreTask(**task_dict)
    cfg = StakeholderAlignmentConfig()
    score, details, labels = orch.stakeholder_alignment(t, cfg, project_stakeholders=task_payload.get("project_stakeholders"))
    await repo.save_alignment(task_payload.get("project_id"), t.id, score, details)
    return {"score": score, "details": details, "labels": labels}
