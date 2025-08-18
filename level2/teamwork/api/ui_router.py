


from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dto import Vote, VoteRequest
from ..orchestrator import TeamworkOrchestrator
from ..dto import VotingConfig, ConflictConfig, StakeholderAlignmentConfig
from ...db.session import get_async_session
from ...db.repo_teamwork import TeamworkRepo

router = APIRouter(prefix="/ui/teamwork", tags=["Teamwork-UI"])
templates = Jinja2Templates(directory="templates")

@router.get("/vote", response_class=HTMLResponse)
async def vote_form(request: Request):
    return templates.TemplateResponse("vote_form.html", {"request": request})

@router.post("/vote", response_class=HTMLResponse)
async def submit_vote(
    request: Request,
    project_id: str = Form(...),
    task_id: str = Form(...),
    voter_id: str = Form(...),
    value: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    vote = Vote(voter_id=voter_id, value=value)
    vr = VoteRequest(project_id=project_id, task_id=task_id, votes=[vote], vote_scheme="binary")
    orch = TeamworkOrchestrator()
    repo = TeamworkRepo(session)

    result, _ = orch.run_voting(vr, VotingConfig())
    await repo.save_voting(project_id, task_id, [vote.dict()], result.dict())

    return templates.TemplateResponse("vote_result.html", {
        "request": request,
        "result": result.dict()
    })

@router.get("/dashboard/{project_id}", response_class=HTMLResponse)
async def dashboard(request: Request, project_id: str, session: AsyncSession = Depends(get_async_session)):
    repo = TeamworkRepo(session)
    records = await repo.get_all_votes(project_id)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "project_id": project_id,
        "records": records
    })


