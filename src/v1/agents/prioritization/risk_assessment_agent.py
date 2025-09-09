

"""
Risk Assessment Agent
"""

from typing import Dict, List
from .models import TaskData

class RiskAssessmentAgent:
    """
    Assesses risks associated with task execution or rejection.
    Analyzes impact, probability of issues, and potential losses.
    """

    def __init__(self):
        self.weights = {
            "uncertainty_level": {"high": 0.7, "medium": 0.4, "low": 0.1},
            "criticality": {"high": 0.6, "medium": 0.3, "low": 0.1},
            "dependency_count": lambda n: min(0.05 * n, 0.3)
        }

    def assess(self, task_data: TaskData) -> Dict:
        """
        Assesses risk for a given task.

        Args:
            task_data: Task data

        Returns:
            Risk assessment results
        """
        risk_score = 0.0
        risk_factors = []

        # Uncertainty level
        unc = task_data.get("uncertainty_level", "medium")
        risk_score += self.weights["uncertainty_level"][unc]
        if unc != "low":
            risk_factors.append(f"Uncertainty: {unc}")

        # Criticality
        crit = task_data.get("criticality", "medium")
        risk_score += self.weights["criticality"][crit]
        if crit == "high":
            risk_factors.append("High criticality")

        # Dependencies
        dep_count = len(task_data.get("dependencies", []))
        risk_score += self.weights["dependency_count"](dep_count)
        if dep_count > 0:
            risk_factors.append(f"{dep_count} dependencies")

        # Risk keywords analysis
        title = task_data.get("title", "").lower()
        description = task_data.get("description", "").lower()
        risk_keywords = ["critical", "urgent", "blocker", "security", "vulnerability", "outage"]

        if any(keyword in title or keyword in description for keyword in risk_keywords):
            risk_score += 0.2
            risk_factors.append("Contains risk keywords")

        # Clamp risk score
        risk_score = min(risk_score, 1.0)

        # Determine risk label
        if risk_score > 0.7:
            label = "high"
        elif risk_score > 0.4:
            label = "medium"
        else:
            label = "low"

        return {
            "risk_score": round(risk_score, 2),
            "risk_factors": risk_factors,
            "risk_label": label
        }

