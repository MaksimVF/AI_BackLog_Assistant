
















from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Optional

from level2.db.models_second_level import async_session, Task, SecondLevelRun, SecondLevelResult

app = FastAPI(title="Second Level Analysis API")


# --- Dependency ---
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# --- Schemas ---
class TaskCreate(BaseModel):
    title: str
    value: Optional[float] = None
    effort: Optional[float] = None


class TaskRead(BaseModel):
    id: int
    title: str
    value: Optional[float]
    effort: Optional[float]

    class Config:
        orm_mode = True


class RunCreate(BaseModel):
    triggered_by: Optional[str] = "system"
    modules: Optional[List[str]] = None


class RunRead(BaseModel):
    id: int
    triggered_by: Optional[str]
    modules: Optional[List[str]]
    status: str

    class Config:
        orm_mode = True


class ResultCreate(BaseModel):
    run_id: int
    module_name: str
    task_id: Optional[int] = None
    result: dict


class ResultRead(BaseModel):
    id: int
    run_id: int
    module_name: str
    task_id: Optional[int]
    result: dict

    class Config:
        orm_mode = True


# --- Endpoints ---

@app.post("/tasks", response_model=TaskRead)
async def create_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    db_task = Task(title=task.title, value=task.value, effort=task.effort)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


@app.get("/tasks", response_model=List[TaskRead])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task))
    return result.scalars().all()


@app.post("/runs", response_model=RunRead)
async def create_run(run: RunCreate, session: AsyncSession = Depends(get_session)):
    db_run = SecondLevelRun(triggered_by=run.triggered_by, modules=run.modules)
    session.add(db_run)
    await session.commit()
    await session.refresh(db_run)
    return db_run


@app.get("/runs", response_model=List[RunRead])
async def get_runs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SecondLevelRun))
    return result.scalars().all()


@app.post("/results", response_model=ResultRead)
async def create_result(res: ResultCreate, session: AsyncSession = Depends(get_session)):
    db_res = SecondLevelResult(
        run_id=res.run_id,
        module_name=res.module_name,
        task_id=res.task_id,
        result=res.result
    )
    session.add(db_res)
    await session.commit()
    await session.refresh(db_res)
    return db_res


@app.get("/results/{task_id}", response_model=List[ResultRead])
async def get_results_for_task(task_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SecondLevelResult).where(SecondLevelResult.task_id == task_id))
    return result.scalars().all()

















