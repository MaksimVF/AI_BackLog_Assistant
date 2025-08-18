





















from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pipelines.first_level_pipeline import FirstLevelPipeline
from pipelines.second_level_pipeline import SecondLevelPipeline
from db.session import get_async_session
from db.models import Task, Run, Result
from db.repo import TaskRepo, RunRepo, ResultRepo
import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/run_pipeline")
async def run_pipeline(tasks: List[dict], session: AsyncSession = Depends(get_async_session)):
    try:
        pipeline = FirstLevelPipeline()
        results = await pipeline.run(tasks)
        return results
    except Exception as e:
        logger.error(f"Error running pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run_second_level")
async def run_second_level(tasks: List[dict], session: AsyncSession = Depends(get_async_session)):
    try:
        pipeline = SecondLevelPipeline()
        results = await pipeline.run(tasks)
        return results
    except Exception as e:
        logger.error(f"Error running second level pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks")
async def create_task(task: Task, session: AsyncSession = Depends(get_async_session)):
    try:
        repo = TaskRepo(session)
        await repo.create(task)
        return {"message": "Task created successfully"}
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks")
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    try:
        repo = TaskRepo(session)
        tasks = await repo.get_all()
        return tasks
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/runs")
async def create_run(run: Run, session: AsyncSession = Depends(get_async_session)):
    try:
        repo = RunRepo(session)
        await repo.create(run)
        return {"message": "Run created successfully"}
    except Exception as e:
        logger.error(f"Error creating run: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/runs")
async def get_runs(session: AsyncSession = Depends(get_async_session)):
    try:
        repo = RunRepo(session)
        runs = await repo.get_all()
        return runs
    except Exception as e:
        logger.error(f"Error getting runs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/results")
async def create_result(result: Result, session: AsyncSession = Depends(get_async_session)):
    try:
        repo = ResultRepo(session)
        await repo.create(result)
        return {"message": "Result created successfully"}
    except Exception as e:
        logger.error(f"Error creating result: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results")
async def get_results(session: AsyncSession = Depends(get_async_session)):
    try:
        repo = ResultRepo(session)
        results = await repo.get_all()
        return results
    except Exception as e:
        logger.error(f"Error getting results: {e}")
        raise HTTPException(status_code=500, detail=str(e))
























