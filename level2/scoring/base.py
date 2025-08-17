

from ..interfaces import ScoringAgent
from ..dto import Task, AnalysisConfig

class BaseScoringAgent(ScoringAgent):
    name = "BASE"

    def score(self, task: Task, cfg: AnalysisConfig):
        raise NotImplementedError

