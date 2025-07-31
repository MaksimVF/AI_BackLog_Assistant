





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
    - Effort vs impact ratio
    - Risk factors
    """

    def __init__(self, critical_threshold: float = 8.0, high_threshold: float = 6.0, medium_threshold: float = 4.0):
        """
        Initialize with configurable thresholds.

        Args:
            critical_threshold: Minimum score for critical classification
            high_threshold: Minimum score for high classification
            medium_threshold: Minimum score for medium classification
        """
        # Threshold configuration
        self.thresholds = {
            "critical": critical_threshold,
            "high": high_threshold,
            "medium": medium_threshold,
            "low": 0,
        }

    def classify(self, task: TaskData) -> Literal["critical", "high", "medium", "low"]:
        """
        Classifies task criticality with enhanced analysis.

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

        # Blocking tasks - increased weight
        if task.get("is_blocking", False):
            score += 2.5

        # Has dependencies
        if task.get("is_dependency", False):
            score += 1.2

        # Effort vs impact analysis
        effort = task.get("effort", 1)
        if effort > 0:
            ratio = impact / effort
            if ratio > 1.5:
                score += 1.5  # High impact, low effort
            elif ratio < 0.5:
                score -= 1.0  # Low impact, high effort

        # Risk factors
        title = task.get("title", "").lower()
        description = task.get("description", "").lower()
        risk_keywords = ["critical", "urgent", "blocker", "security", "vulnerability", "outage"]
        if any(keyword in title or keyword in description for keyword in risk_keywords):
            score += 1.8

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
        Provides detailed explanation for criticality classification.

        Args:
            task: Task data

        Returns:
            Detailed explanation string
        """
        status = self.classify(task)
        impact = task.get("impact", 0)
        urgency = task.get("urgency", 0)
        is_blocking = task.get("is_blocking", False)
        is_dependency = task.get("is_dependency", False)
        effort = task.get("effort", 1)
        ratio = impact / effort if effort > 0 else 0

        reasons = []

        # Impact and urgency
        if impact > 7:
            reasons.append(f"high impact ({impact})")
        elif impact > 4:
            reasons.append(f"moderate impact ({impact})")

        if urgency > 7:
            reasons.append(f"high urgency ({urgency})")
        elif urgency > 4:
            reasons.append(f"moderate urgency ({urgency})")

        # Blocking and dependencies
        if is_blocking:
            reasons.append("blocks other tasks")
        if is_dependency:
            reasons.append("has dependencies")

        # Effort-impact ratio
        if ratio > 1.5:
            reasons.append(f"high impact/effort ratio ({ratio:.2f})")
        elif ratio < 0.5:
            reasons.append(f"low impact/effort ratio ({ratio:.2f})")

        # Risk factors
        title = task.get("title", "").lower()
        description = task.get("description", "").lower()
        risk_keywords = ["critical", "urgent", "blocker", "security", "vulnerability", "outage"]
        if any(keyword in title or keyword in description for keyword in risk_keywords):
            reasons.append("contains risk keywords")

        explanation = f"Classified as '{status}' based on: {', '.join(reasons)}"
        return explanation





