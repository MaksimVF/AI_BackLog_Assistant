


"""
Deadline Sensitivity Agent
"""

from typing import Dict, List
from datetime import datetime
from .models import TaskData

class DeadlineSensitivityAgent:
    """
    Evaluates task urgency and deadline impact on the overall project.
    Considers both importance and time constraints.
    """

    def __init__(self):
        pass

    def assess(self, task_data: TaskData) -> Dict:
        """
        Assesses deadline sensitivity for a given task.

        Args:
            task_data: Task data

        Returns:
            Deadline sensitivity assessment
        """
        reasons = []
        urgency = "low"

        # Check for deadline
        deadline_str = task_data.get("deadline")
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                today = datetime.now()
                delta = (deadline - today).days

                if delta <= 1:
                    urgency = "high"
                    reasons.append(f"Deadline in {delta} day(s)")
                elif delta <= 3:
                    urgency = "medium"
                    reasons.append(f"Deadline approaching in {delta} days")
            except ValueError:
                pass

        # Check task type
        task_type = task_data.get("type", "").lower()
        if task_type in ["bug", "incident", "blocker"]:
            if urgency != "high":
                urgency = "medium"
            reasons.append(f"Task type: {task_type}")

        # Check for critical path
        if task_data.get("is_blocking", False):
            urgency = "high"
            reasons.append("Blocks other tasks")

        # Check for external dependencies
        external_deps = task_data.get("external_dependencies", [])
        if external_deps:
            urgency = "medium"
            reasons.append(f"Has external dependencies: {', '.join(external_deps)}")

        return {
            "urgency_label": urgency,
            "urgency_reasons": reasons
        }



