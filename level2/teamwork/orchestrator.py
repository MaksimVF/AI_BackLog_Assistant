




from typing import List, Dict, Any
from .agents.voting_consensus import VotingConsensusAgent
from .agents.conflict_resolution import ConflictResolutionAgent
from .agents.stakeholder_alignment import StakeholderAlignmentAgent
from ..teamwork.dto import VotingConfig, ConflictConfig, StakeholderAlignmentConfig
from level2.dto import Task

class TeamworkOrchestrator:
    def __init__(self):
        self.voting = VotingConsensusAgent()
        self.conflict = ConflictResolutionAgent()
        self.stakeholder = StakeholderAlignmentAgent()

    def run_voting(self, vote_req, cfg=None):
        cfg = cfg or VotingConfig()
        result, internals = self.voting.score(vote_req, cfg)
        return result, internals

    def analyze_conflict(self, vote_req, cfg=None):
        cfg = cfg or ConflictConfig()
        severity, details = self.conflict.score(vote_req, cfg)
        return severity, details

    def stakeholder_alignment(self, task: Task, cfg=None, project_stakeholders: Dict[str, Dict[str, Any]] = None):
        cfg = cfg or StakeholderAlignmentConfig()
        if project_stakeholders is None:
            project_stakeholders = task.metadata.get("project_stakeholders")
        score, details, labels = self.stakeholder.score(task, cfg, project_stakeholders)
        return score, details, labels



