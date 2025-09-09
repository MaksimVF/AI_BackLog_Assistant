


"""
Resource Availability Agent
"""

from typing import Dict, List
from .models import TaskData

class ResourceAvailabilityAgent:
    """
    Analyzes availability of required resources for task implementation.
    Considers human, technical, and time resources.
    """

    def __init__(self):
        self.skill_weight = {"high": 1.0, "medium": 0.6, "low": 0.2}

    def assess(self, task_data: TaskData) -> Dict:
        """
        Assesses resource availability for a given task.

        Args:
            task_data: Task data

        Returns:
            Resource availability assessment
        """
        score = 0.0
        gaps = []

        # Skill analysis
        required_skills = task_data.get("required_skills", [])
        expertise = task_data.get("team_expertise", {})
        skill_score = 0

        for skill in required_skills:
            level = expertise.get(skill, "low")
            skill_score += self.skill_weight[level]
            if level == "low":
                gaps.append(f"{skill}: low expertise")

        if required_skills:
            skill_score /= len(required_skills)
        else:
            skill_score = 1.0  # No skills specified, assume no constraints

        # Time analysis
        time_ratio = min(task_data.get("available_hours", 0) / task_data.get("estimated_time_hours", 1), 1.0)
        if time_ratio < 0.5:
            gaps.append("Insufficient time available")

        # Budget analysis
        budget_ratio = min(task_data.get("budget_available", 0) / task_data.get("budget_required", 1), 1.0)
        if budget_ratio < 1.0:
            gaps.append("Insufficient budget")

        # Final score calculation
        score = 0.5 * skill_score + 0.25 * time_ratio + 0.25 * budget_ratio

        # Determine resource label
        if score > 0.75:
            label = "sufficient"
        elif score > 0.5:
            label = "partial"
        else:
            label = "insufficient"

        return {
            "resource_score": round(score, 2),
            "resource_gaps": gaps,
            "resource_label": label
        }


