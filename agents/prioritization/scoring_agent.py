




"""
Scoring Agent for ICE/RICE Prioritization
"""

from typing import Dict, Optional
from .models import TaskData, PriorityScore
from .effort_estimator import EffortEstimatorAgent

class ScoringAgent:
    """
    Calculates ICE and RICE scores for tasks.
    Automatically estimates missing parameters when needed.
    """

    def __init__(self):
        self.effort_estimator = EffortEstimatorAgent()

    def _ensure_params(self, task: TaskData) -> TaskData:
        """
        Ensures all required parameters are present by estimating missing ones.
        """
        if task.get("effort") is None:
            task["effort"] = self.effort_estimator.estimate_effort(task)

        if task.get("impact") is None:
            task["impact"] = 5  # Default medium impact

        if task.get("confidence") is None:
            task["confidence"] = 0.8  # Default 80% confidence

        return task

    def calculate_score(self, task: TaskData, model: str = "RICE") -> PriorityScore:
        """
        Calculates ICE or RICE score for a task.

        Args:
            task: Task data
            model: "ICE" or "RICE" (default: "RICE")

        Returns:
            PriorityScore with calculated values
        """
        task = self._ensure_params(task)

        impact = task["impact"]
        confidence = task["confidence"]
        effort = task["effort"]

        if model == "ICE":
            score = (impact * confidence) / effort
            return {
                "score_type": "ICE",
                "score": round(score, 2),
                "impact": impact,
                "confidence": confidence,
                "effort": effort
            }
        elif model == "RICE":
            reach = task.get("reach", 100)  # Default reach
            score = (reach * impact * confidence) / effort
            return {
                "score_type": "RICE",
                "score": round(score, 2),
                "reach": reach,
                "impact": impact,
                "confidence": confidence,
                "effort": effort
            }
        else:
            raise ValueError(f"Unsupported scoring model: {model}")

    def score_task(self, task: TaskData) -> PriorityScore:
        """
        Scores a task using RICE model by default.
        """
        return self.calculate_score(task, "RICE")




