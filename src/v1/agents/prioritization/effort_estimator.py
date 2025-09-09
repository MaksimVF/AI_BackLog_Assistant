






"""
Effort Estimation Agent
"""

from typing import Dict
from .models import TaskData

class EffortEstimatorAgent:
    """
    Estimates effort for tasks using heuristics and LLM.
    Falls back to rule-based estimation when LLM is not available.
    """

    def __init__(self, llm_client=None):
        self.llm = llm_client

    def estimate_effort(self, task: TaskData) -> int:
        """
        Estimates effort based on task title and description.
        Uses LLM if available, otherwise falls back to heuristics.

        Args:
            task: Task data

        Returns:
            Estimated effort (1-10 scale)
        """
        if self.llm:
            return self._estimate_with_llm(task)
        else:
            return self._estimate_with_heuristics(task)

    def _estimate_with_llm(self, task: TaskData) -> int:
        """
        Estimates effort using LLM.
        """
        prompt = f"""
Analyze the following task and estimate the effort required on a scale of 1-10:
1-2: Very low effort (minutes to an hour)
3-4: Low effort (few hours)
5-6: Medium effort (half day to a day)
7-8: High effort (2-3 days)
9-10: Very high effort (week or more)

Task Title: {task.get('title', '')}
Task Description: {task.get('description', '')}

Provide only the number (1-10):
"""

        try:
            response = self.llm(prompt)
            # Extract number from response
            import re
            match = re.search(r'(\d+)', response)
            if match:
                effort = int(match.group(1))
                return max(1, min(10, effort))  # Clamp to 1-10
        except Exception:
            pass

        # Fallback to heuristics if LLM fails
        return self._estimate_with_heuristics(task)

    def _estimate_with_heuristics(self, task: TaskData) -> int:
        """
        Estimates effort using rule-based heuristics.
        """
        description = (task.get("description", "") + " " + task.get("title", "")).lower()

        # Enhanced keyword-based estimation
        complex_keywords = ["api", "auth", "integration", "deployment", "architecture", "database"]
        medium_keywords = ["ui", "form", "component", "service", "module"]
        simple_keywords = ["fix", "bug", "typo", "error", "text", "style"]

        if any(keyword in description for keyword in complex_keywords):
            return 5 if "migration" not in description else 7
        elif any(keyword in description for keyword in medium_keywords):
            return 4
        elif any(keyword in description for keyword in simple_keywords):
            return 2 if "critical" not in description else 3
        else:
            # Estimate based on description length as proxy for complexity
            desc_length = len(description)
            if desc_length > 200:
                return 6
            elif desc_length > 100:
                return 4
            else:
                return 3

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






