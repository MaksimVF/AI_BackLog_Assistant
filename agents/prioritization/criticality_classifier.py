





"""
Criticality Classification Agent
"""

from typing import Literal
from .models import TaskData

class CriticalityClassifierAgent:
    """
    Classifies task criticality based on:
    - Impact
    - Urgency
    - Blocking status
    - Dependencies
    """

    def __init__(self):
        # Threshold configuration
        self.thresholds = {
            "critical": 8,
            "high": 6,
            "medium": 4,
            "low": 0,
        }

    def classify(self, task: TaskData) -> Literal["critical", "high", "medium", "low"]:
        """
        Classifies task criticality.

        Args:
            task: Task data

        Returns:
            Criticality level
        """
        score = 0

        # Impact contribution
        impact = task.get("impact", 0)
        score += 0.5 * impact

        # Urgency contribution
        urgency = task.get("urgency", 0)
        score += 0.5 * urgency

        # Blocking tasks
        if task.get("is_blocking", False):
            score += 2

        # Has dependencies
        if task.get("is_dependency", False):
            score += 1

        # Determine criticality level
        if score >= self.thresholds["critical"]:
            return "critical"
        elif score >= self.thresholds["high"]:
            return "high"
        elif score >= self.thresholds["medium"]:
            return "medium"
        else:
            return "low"

    def explain(self, task: TaskData) -> str:
        """
        Provides explanation for criticality classification.
        """
        status = self.classify(task)
        impact = task.get("impact", 0)
        urgency = task.get("urgency", 0)
        is_blocking = task.get("is_blocking", False)
        is_dependency = task.get("is_dependency", False)

        reasons = [
            f"impact={impact}",
            f"urgency={urgency}",
            f"blocking={is_blocking}",
            f"dependency={is_dependency}"
        ]

        return f"Classified as '{status}' based on: {', '.join(reasons)}"





