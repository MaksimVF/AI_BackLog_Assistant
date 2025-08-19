


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from level2.db.session import AsyncSessionLocal as async_session
# Note: Task model is not available, using task_id as string instead

from db_third_level import ThirdLevelRun, ThirdLevelResult, DecisionFeedback
from agents.third_level.decision_recommender import DecisionRecommenderAgent
from agents.third_level.scenario_simulation import ScenarioSimulationAgent, ScenarioChange

router = APIRouter(prefix="/third-level", tags=["third-level"])

# --- dependency ---
async def get_session() -> AsyncSession:
    async with async_session() as s:
        yield s

# --- schemas ---
class RecommendRequest(BaseModel):
    triggered_by: Optional[str] = "system"

class RecommendResponse(BaseModel):
    run_id: int

class ScenarioChangeIn(BaseModel):
    action: Literal["drop", "delay", "accelerate", "modify"]
    task_id: Optional[str] = None
    delta_value: Optional[float] = None
    delta_effort: Optional[float] = None

class ScenarioRequest(BaseModel):
    tasks: List[dict] = Field(..., description="Список задач (id, title, value, effort, ...)")
    changes: List[ScenarioChangeIn]

class ScenarioResponse(BaseModel):
    baseline: dict
    scenario: dict
    delta: dict
    result_tasks: List[dict]

class DecisionActionRequest(BaseModel):
    user_id: Optional[str] = None
    decision: Literal["accepted", "rejected"]
    feedback: Optional[str] = None

class ThirdLevelResultRead(BaseModel):
    id: int
    run_id: int
    task_id: Optional[str]
    recommendation: str
    explanation: Optional[str]
    confidence: Optional[float]

    class Config:
        from_attributes = True

# --- endpoints ---

@router.post("/recommend", response_model=RecommendResponse)
async def recommend(payload: RecommendRequest, session: AsyncSession = Depends(get_session)):
    agent = DecisionRecommenderAgent()
    run_id = await agent.run(session, triggered_by=payload.triggered_by)
    return RecommendResponse(run_id=run_id)

@router.get("/results/{run_id}", response_model=List[ThirdLevelResultRead])
async def get_results(run_id: int, session: AsyncSession = Depends(get_session)):
    q = await session.execute(
        select(ThirdLevelResult).where(ThirdLevelResult.run_id == run_id)
    )
    return q.scalars().all()

@router.post("/scenario", response_model=ScenarioResponse)
async def simulate(payload: ScenarioRequest):
    agent = ScenarioSimulationAgent()
    changes = [ScenarioChange(**c.dict()) for c in payload.changes]
    result = agent.run(payload.tasks, changes)
    return ScenarioResponse(**result)

@router.post("/confirm/{result_id}")
async def confirm_decision(result_id: int, payload: DecisionActionRequest, session: AsyncSession = Depends(get_session)):
    # контроль, что результат существует
    q = await session.execute(select(ThirdLevelResult).where(ThirdLevelResult.id == result_id))
    res = q.scalar_one_or_none()
    if not res:
        raise HTTPException(status_code=404, detail="Result not found")

    fb = DecisionFeedback(
        result_id=result_id,
        user_id=payload.user_id,
        decision=payload.decision,
        feedback=payload.feedback
    )
    session.add(fb)
    await session.commit()
    return {"status": "ok"}



