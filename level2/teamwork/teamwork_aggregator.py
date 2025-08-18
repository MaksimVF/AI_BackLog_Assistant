












from typing import List, Dict, Any, Optional
from .voting_consensus import VotingConsensusAgent
from .conflict_resolution import ConflictResolutionAgent
from .stakeholder_alignment import StakeholderAlignmentAgent

class TeamworkAggregator:
    """
    Агрегатор для модулей командной работы (второй уровень).
    Координирует работу агентов Voting, Consensus, Conflict Resolution, Stakeholder Alignment.
    """

    def __init__(self):
        self.voting_agent = VotingConsensusAgent()
        self.conflict_agent = ConflictResolutionAgent()
        self.stakeholder_agent = StakeholderAlignmentAgent()

    async def run(self, tasks: List[Dict], votes: Dict = None) -> Dict[str, Any]:
        """
        Запуск всех доступных агентов командной работы.
        :param tasks: список задач
        :param votes: данные для голосования
        :return: агрегированные результаты
        """
        results = {}

        if votes:
            results["voting"] = await self.voting_agent.run(votes)

        results["conflicts"] = await self.conflict_agent.run(tasks)
        results["stakeholder_alignment"] = await self.stakeholder_agent.run(tasks)

        return results












