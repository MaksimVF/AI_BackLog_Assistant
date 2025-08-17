



from .base import BaseScoringAgent
from ..dto import Task, AnalysisConfig

MOSCOW_MAP = {"must": 1.0, "should": 0.8, "could": 0.5, "wont": 0.0}

class MoSCoWAgent(BaseScoringAgent):
    name = "MOSCOW"

    def score(self, task, cfg):
        label = task.metadata.get("moscow", "could").lower()
        score = MOSCOW_MAP.get(label, 0.5)
        return score, {"label": label}, {"MOSCOW": label}



