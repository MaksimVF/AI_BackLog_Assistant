
























from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from db.models import Task, Run, Result
from typing import List, Optional
import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TaskRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: Task):
        try:
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            raise

    async def get_all(self) -> List[Task]:
        try:
            result = await self.session.execute(select(Task))
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting tasks: {e}")
            raise

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        try:
            result = await self.session.execute(select(Task).where(Task.id == task_id))
            return result.scalar_one_or_none()
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
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            raise

class RunRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, run: Run):
        try:
            self.session.add(run)
            await self.session.commit()
            await self.session.refresh(run)
        except Exception as e:
            logger.error(f"Error creating run: {e}")
            raise

    async def get_all(self) -> List[Run]:
        try:
            result = await self.session.execute(select(Run))
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting runs: {e}")
            raise

    async def get_by_id(self, run_id: int) -> Optional[Run]:
        try:
            result = await self.session.execute(select(Run).where(Run.id == run_id))
            return result.scalar_one_or_none()
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
        except Exception as e:
            logger.error(f"Error deleting run: {e}")
            raise

class ResultRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, result: Result):
        try:
            self.session.add(result)
            await self.session.commit()
            await self.session.refresh(result)
        except Exception as e:
            logger.error(f"Error creating result: {e}")
            raise

    async def get_all(self) -> List[Result]:
        try:
            result = await self.session.execute(select(Result))
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting results: {e}")
            raise

    async def get_by_id(self, result_id: int) -> Optional[Result]:
        try:
            result = await self.session.execute(select(Result).where(Result.id == result_id))
            return result.scalar_one_or_none()
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
        except Exception as e:
            logger.error(f"Error deleting result: {e}")
            raise



























