




























from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pipelines.first_level_pipeline import FirstLevelPipeline
from pipelines.second_level_pipeline import SecondLevelPipeline
from db.session import get_async_session
from db.models import Task, Run, Result, User
from db.repo_optimized import TaskRepo, RunRepo, ResultRepo, UserRepo
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import aioredis
import os
from api.auth import get_current_user, get_current_admin_user
from api.validation import TaskCreate, TaskUpdate, RunCreate, RunUpdate, ResultCreate, ResultUpdate, UserCreate, UserUpdate, UserLogin

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(default_response_class=ORJSONResponse)

# Middleware для CORS и GZip
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Настройка Redis для кэширования
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.post("/run_pipeline")
async def run_pipeline(tasks: List[dict], session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    try:
        pipeline = FirstLevelPipeline()
        results = await pipeline.run(tasks)
        return results
    except Exception as e:
        logger.error(f"Error running pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run_second_level")
async def run_second_level(tasks: List[dict], session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    try:
        pipeline = SecondLevelPipeline()
        results = await pipeline.run(tasks)
        return results
    except Exception as e:
        logger.error(f"Error running second level pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks")
async def create_task(task: TaskCreate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    try:
        repo = TaskRepo(session)
        task_dict = task.dict()
        task_obj = Task(**task_dict)
        await repo.create(task_obj)
        return {"message": "Task created successfully"}
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks")
@cache(expire=60)
async def get_tasks(session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    try:
        repo = TaskRepo(session)
        tasks = await repo.get_all()
        return tasks
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/runs")
async def create_run(run: RunCreate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    try:
        repo = RunRepo(session)
        run_dict = run.dict()
        run_obj = Run(**run_dict)
        await repo.create(run_obj)
        return {"message": "Run created successfully"}
    except Exception as e:
        logger.error(f"Error creating run: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/runs")
@cache(expire=60)
async def get_runs(session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    try:
        repo = RunRepo(session)
        runs = await repo.get_all()
        return runs
    except Exception as e:
        logger.error(f"Error getting runs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/results")
async def create_result(result: ResultCreate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    try:
        repo = ResultRepo(session)
        result_dict = result.dict()
        result_obj = Result(**result_dict)
        await repo.create(result_obj)
        return {"message": "Result created successfully"}
    except Exception as e:
        logger.error(f"Error creating result: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results")
@cache(expire=60)
async def get_results(session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    try:
        repo = ResultRepo(session)
        results = await repo.get_all()
        return results
    except Exception as e:
        logger.error(f"Error getting results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users")
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_admin_user)):
    try:
        repo = UserRepo(session)
        user_dict = user.dict()
        user_obj = User(**user_dict)
        await repo.create(user_obj)
        return {"message": "User created successfully"}
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
@cache(expire=60)
async def get_users(session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_admin_user)):
    try:
        repo = UserRepo(session)
        users = await repo.get_all()
        return users
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_admin_user)):
    try:
        repo = UserRepo(session)
        user_dict = user.dict(exclude_unset=True)
        user_obj = await repo.update(user_id, user_dict)
        return {"message": "User updated successfully"}
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_admin_user)):
    try:
        repo = UserRepo(session)
        await repo.delete(user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail=str(e))































