

























from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from db.models import Task, Run, Result
from typing import List, Optional
import logging
import aioredis
import json
import os

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Настройка Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class Cache:
    def __init__(self, redis_url: str = REDIS_URL):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        if self.redis is None:
            self.redis = await aioredis.create_redis_pool(self.redis_url)

    async def close(self):
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()

    async def get(self, key: str):
        if self.redis is None:
            await self.connect()
        try:
            value = await self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None

    async def set(self, key: str, value, expire: int = 3600):
        if self.redis is None:
            await self.connect()
        try:
            await self.redis.set(key, json.dumps(value), expire=expire)
        except Exception as e:
            logger.error(f"Error setting cache: {e}")

    async def delete(self, key: str):
        if self.redis is None:
            await self.connect()
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")

class TaskRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.cache = Cache()

    async def create(self, task: Task):
        try:
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)
            # Очистка кэша
            await self.cache.delete(f"tasks_all")
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            raise

    async def get_all(self) -> List[Task]:
        try:
            # Проверка кэша
            cached_tasks = await self.cache.get(f"tasks_all")
            if cached_tasks:
                return cached_tasks
            result = await self.session.execute(select(Task))
            tasks = result.scalars().all()
            # Сохранение в кэш
            await self.cache.set(f"tasks_all", tasks)
            return tasks
        except Exception as e:
            logger.error(f"Error getting tasks: {e}")
            raise

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        try:
            # Проверка кэша
            cached_task = await self.cache.get(f"task_{task_id}")
            if cached_task:
                return cached_task
            result = await self.session.execute(select(Task).where(Task.id == task_id))
            task = result.scalar_one_or_none()
            if task:
                # Сохранение в кэш
                await self.cache.set(f"task_{task_id}", task)
            return task
        except Exception as e:
            logger.error(f"Error getting task by id: {e}")
            raise

    async def update(self, task_id: int, task_data: dict):
        try:
            task = await self.get_by_id(task_id)
            if task:
                for key, value in task_data.items():
                    setattr(task, key, value)
                await self.session.commit()
                await self.session.refresh(task)
                # Очистка кэша
                await self.cache.delete(f"task_{task_id}")
                await self.cache.delete(f"tasks_all")
            return task
        except Exception as e:
            logger.error(f"Error updating task: {e}")
            raise

    async def delete(self, task_id: int):
        try:
            task = await self.get_by_id(task_id)
            if task:
                await self.session.delete(task)
                await self.session.commit()
                # Очистка кэша
                await self.cache.delete(f"task_{task_id}")
                await self.cache.delete(f"tasks_all")
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            raise

class RunRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.cache = Cache()

    async def create(self, run: Run):
        try:
            self.session.add(run)
            await self.session.commit()
            await self.session.refresh(run)
            # Очистка кэша
            await self.cache.delete(f"runs_all")
        except Exception as e:
            logger.error(f"Error creating run: {e}")
            raise

    async def get_all(self) -> List[Run]:
        try:
            # Проверка кэша
            cached_runs = await self.cache.get(f"runs_all")
            if cached_runs:
                return cached_runs
            result = await self.session.execute(select(Run))
            runs = result.scalars().all()
            # Сохранение в кэш
            await self.cache.set(f"runs_all", runs)
            return runs
        except Exception as e:
            logger.error(f"Error getting runs: {e}")
            raise

    async def get_by_id(self, run_id: int) -> Optional[Run]:
        try:
            # Проверка кэша
            cached_run = await self.cache.get(f"run_{run_id}")
            if cached_run:
                return cached_run
            result = await self.session.execute(select(Run).where(Run.id == run_id))
            run = result.scalar_one_or_none()
            if run:
                # Сохранение в кэш
                await self.cache.set(f"run_{run_id}", run)
            return run
        except Exception as e:
            logger.error(f"Error getting run by id: {e}")
            raise

    async def update(self, run_id: int, run_data: dict):
        try:
            run = await self.get_by_id(run_id)
            if run:
                for key, value in run_data.items():
                    setattr(run, key, value)
                await self.session.commit()
                await self.session.refresh(run)
                # Очистка кэша
                await self.cache.delete(f"run_{run_id}")
                await self.cache.delete(f"runs_all")
            return run
        except Exception as e:
            logger.error(f"Error updating run: {e}")
            raise

    async def delete(self, run_id: int):
        try:
            run = await self.get_by_id(run_id)
            if run:
                await self.session.delete(run)
                await self.session.commit()
                # Очистка кэша
                await self.cache.delete(f"run_{run_id}")
                await self.cache.delete(f"runs_all")
        except Exception as e:
            logger.error(f"Error deleting run: {e}")
            raise

class ResultRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.cache = Cache()

    async def create(self, result: Result):
        try:
            self.session.add(result)
            await self.session.commit()
            await self.session.refresh(result)
            # Очистка кэша
            await self.cache.delete(f"results_all")
        except Exception as e:
            logger.error(f"Error creating result: {e}")
            raise

    async def get_all(self) -> List[Result]:
        try:
            # Проверка кэша
            cached_results = await self.cache.get(f"results_all")
            if cached_results:
                return cached_results
            result = await self.session.execute(select(Result))
            results = result.scalars().all()
            # Сохранение в кэш
            await self.cache.set(f"results_all", results)
            return results
        except Exception as e:
            logger.error(f"Error getting results: {e}")
            raise

    async def get_by_id(self, result_id: int) -> Optional[Result]:
        try:
            # Проверка кэша
            cached_result = await self.cache.get(f"result_{result_id}")
            if cached_result:
                return cached_result
            result = await self.session.execute(select(Result).where(Result.id == result_id))
            result = result.scalar_one_or_none()
            if result:
                # Сохранение в кэш
                await self.cache.set(f"result_{result_id}", result)
            return result
        except Exception as e:
            logger.error(f"Error getting result by id: {e}")
            raise

    async def update(self, result_id: int, result_data: dict):
        try:
            result = await self.get_by_id(result_id)
            if result:
                for key, value in result_data.items():
                    setattr(result, key, value)
                await self.session.commit()
                await self.session.refresh(result)
                # Очистка кэша
                await self.cache.delete(f"result_{result_id}")
                await self.cache.delete(f"results_all")
            return result
        except Exception as e:
            logger.error(f"Error updating result: {e}")
            raise

    async def delete(self, result_id: int):
        try:
            result = await self.get_by_id(result_id)
            if result:
                await self.session.delete(result)
                await self.session.commit()
                # Очистка кэша
                await self.cache.delete(f"result_{result_id}")
                await self.cache.delete(f"results_all")
        except Exception as e:
            logger.error(f"Error deleting result: {e}")
            raise





























