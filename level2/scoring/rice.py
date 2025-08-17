


from .base import BaseScoringAgent
from ..dto import Task, AnalysisConfig

class RiceAgent(BaseScoringAgent):
    name = "RICE"

    def score(self, task: Task, cfg: AnalysisConfig):
        reach = task.reach or 0
        impact = task.impact or 0
        confidence = task.confidence or 0
        effort = task.effort or 1e-6
        rice = (reach * impact * confidence) / effort
        return rice, {"reach": reach, "impact": impact, "confidence": confidence, "effort": effort}, {}


