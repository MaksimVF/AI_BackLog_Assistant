



from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from .models_teamwork import VotingRecord, ConflictRecord, StakeholderAlignmentRecord, PredictiveAnalysisSnapshot

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

    async def save_predictive_analysis(self, project_id, task_id, agent, score, details, labels):
        rec = PredictiveAnalysisSnapshot(
            project_id=project_id,
            task_id=task_id,
            agent=agent,
            score=score,
            details=details,
            labels=labels
        )
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    async def get_all_votes(self, project_id: str):
        q = select(VotingRecord).where(VotingRecord.project_id == project_id)
        res = await self.session.execute(q)
        return res.scalars().all()

    async def build_votes_matrix(self, project_id: str, latest_only: bool = True):
        """
        Returns (task_ids, voter_ids, matrix)
        matrix[i][j] — sum of votes from voter j on task i (normalized to roughly [-1..1]).
        latest_only: if True, use only the latest vote for each (task,voter) pair.
        """
        records = await self.get_all_votes(project_id)
        # Collect all votes in time order (if latest_only, later votes override previous ones)
        # Format: record.votes — list of dicts: {"voter_id":..,"value":..,"weight":..}
        # Build map: (task_id, voter_id) -> numeric_value * weight
        cell_map = {}
        voters_set = set()
        tasks_set = set()

        for rec in records:
            task_id = rec.task_id
            tasks_set.add(task_id)
            votes = rec.votes or []
            for v in votes:
                voter_id = v.get("voter_id")
                voters_set.add(voter_id)
                # Normalize value: "yes"->1, "no"->-1, "abstain"/None->0, numeric preserved
                raw = v.get("value")
                try:
                    if isinstance(raw, str):
                        rs = raw.strip().lower()
                        if rs in ("yes","y","approve","1","true"):
                            val = 1.0
                        elif rs in ("no","n","reject","0","false"):
                            val = -1.0
                        else:
                            # try numeric
                            val = float(raw)
                    else:
                        val = float(raw)
                except Exception:
                    val = 0.0
                weight = float(v.get("weight") or 1.0)
                score = val * weight
                key = (task_id, voter_id)
                # if latest_only, override; else sum
                if latest_only:
                    cell_map[key] = score
                else:
                    cell_map[key] = cell_map.get(key, 0.0) + score

        task_ids = sorted(list(tasks_set))
        voter_ids = sorted(list(voters_set))
        # Build matrix
        matrix = []
        for t in task_ids:
            row = []
            for v in voter_ids:
                val = cell_map.get((t,v), 0.0)
                # Threshold/normalize: limit extreme weights
                if val > 1.0:
                    val = 1.0
                if val < -1.0:
                    val = -1.0
                row.append(val)
            matrix.append(row)
        return task_ids, voter_ids, matrix




