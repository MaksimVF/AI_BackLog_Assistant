


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import StrategicAnalysisSnapshot

class StrategicRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_snapshot(self, snapshot: StrategicAnalysisSnapshot):
        self.session.add(snapshot)
        await self.session.commit()
        await self.session.refresh(snapshot)
        return snapshot

    async def get_snapshots(self, project_id: str, task_id: str = None):
        stmt = select(StrategicAnalysisSnapshot).where(StrategicAnalysisSnapshot.project_id == project_id)
        if task_id:
            stmt = stmt.where(StrategicAnalysisSnapshot.task_id == task_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


