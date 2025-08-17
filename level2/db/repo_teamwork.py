





from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from .models_teamwork import VotingRecord, ConflictRecord, StakeholderAlignmentRecord

class TeamworkRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_voting(self, project_id, task_id, votes, result):
        rec = VotingRecord(project_id=project_id, task_id=task_id, votes=votes, result=result)
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    async def save_conflict(self, project_id, task_id, analysis, severity):
        rec = ConflictRecord(project_id=project_id, task_id=task_id, analysis=analysis, severity=severity)
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    async def save_alignment(self, project_id, task_id, score, details):
        rec = StakeholderAlignmentRecord(project_id=project_id, task_id=task_id, score=score, details=details)
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec





