






"""
Effort Estimation Agent
"""

from typing import Dict
from .models import TaskData

class EffortEstimatorAgent:
    """
    Estimates effort for tasks based on heuristics.
    Can be extended with LLM integration later.
    """

    def estimate_effort(self, task: TaskData) -> int:
        """
        Estimates effort based on task title and description.

        Args:
            task: Task data

        Returns:
            Estimated effort (1-10 scale)
        """
        description = (task.get("description", "") + " " + task.get("title", "")).lower()

        # Keyword-based estimation
        if any(keyword in description for keyword in ["api", "auth", "integration", "deployment"]):
            return 5
        elif any(keyword in description for keyword in ["ui", "button", "form", "text"]):
            return 3
        elif any(keyword in description for keyword in ["fix", "bug", "typo", "error"]):
            return 2
        elif any(keyword in description for keyword in ["refactor", "restructure", "clean"]):
            return 4
        else:
            return 6  # Default medium effort

    def estimate_impact(self, task: TaskData) -> int:
        """
        Estimates impact based on task description.

        Args:
            task: Task data

        Returns:
            Estimated impact (1-10 scale)
        """
        description = (task.get("description", "") + " " + task.get("title", "")).lower()

        if any(keyword in description for keyword in ["critical", "urgent", "blocker", "security"]):
            return 8
        elif any(keyword in description for keyword in ["important", "major", "core"]):
            return 6
        elif any(keyword in description for keyword in ["minor", "small", "cosmetic"]):
            return 3
        else:
            return 5  # Default medium impact

    def estimate_confidence(self, task: TaskData) -> float:
        """
        Estimates confidence based on task completeness.

        Args:
            task: Task data

        Returns:
            Estimated confidence (0.1-1.0)
        """
        description = (task.get("description", "") + " " + task.get("title", "")).lower()

        # If description is detailed, higher confidence
        if len(description) > 100:
            return 0.9
        elif len(description) > 50:
            return 0.7
        else:
            return 0.5

    def estimate_reach(self, task: TaskData) -> int:
        """
        Estimates reach based on task description.

        Args:
            task: Task data

        Returns:
            Estimated reach (number of users/systems affected)
        """
        description = (task.get("description", "") + " " + task.get("title", "")).lower()

        if any(keyword in description for keyword in ["all users", "entire system", "global"]):
            return 1000
        elif any(keyword in description for keyword in ["most users", "majority", "core feature"]):
            return 500
        elif any(keyword in description for keyword in ["some users", "minor feature", "edge case"]):
            return 100
        else:
            return 200  # Default reach






