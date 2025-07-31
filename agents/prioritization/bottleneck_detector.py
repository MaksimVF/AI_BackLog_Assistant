





"""
Bottleneck Detection Agent
"""

from typing import List, Dict, Optional
from .models import TaskData

class BottleneckDetectorAgent:
    """
    Detects potential bottlenecks in tasks based on:
    - High effort relative to impact
    - Blocking dependencies
    - Low confidence
    - Task dependencies and critical path analysis
    - Risk factors
    """

    def __init__(self, score_threshold: float = 3.0, effort_impact_ratio: float = 0.5):
        """
        Initialize with configurable thresholds.

        Args:
            score_threshold: Minimum score to avoid bottleneck classification
            effort_impact_ratio: Minimum acceptable impact/effort ratio
        """
        self.score_threshold = score_threshold
        self.effort_impact_ratio = effort_impact_ratio

    def detect_bottlenecks(self, task: TaskData) -> List[str]:
        """
        Detects bottlenecks for a single task with enhanced analysis.

        Args:
            task: Task data with scoring information

        Returns:
            List of bottleneck descriptions
        """
        bottlenecks = []

        # Check for low score
        score = task.get("score", {}).get("score", self.score_threshold + 1)
        if score < self.score_threshold:
            bottlenecks.append(f"Low priority score: {score}")

        # Enhanced effort vs impact analysis
        effort = task.get("effort", 1)
        impact = task.get("impact", 1)
        if effort > 0:
            ratio = impact / effort
            if ratio < self.effort_impact_ratio:
                bottlenecks.append(f"High effort relative to impact (ratio: {ratio:.2f})")
            if effort > 8 and impact < 5:
                bottlenecks.append("Very high effort for low impact task")

        # Enhanced dependency analysis
        blocks_count = task.get("blocks_count", 0)
        if blocks_count > 2:
            bottlenecks.append(f"Blocks {blocks_count} other tasks")
        elif blocks_count > 0 and task.get("is_blocking", False):
            bottlenecks.append(f"Blocks {blocks_count} task(s) in critical path")

        # Check confidence with more granularity
        confidence = task.get("confidence", 1)
        if confidence < 0.3:
            bottlenecks.append(f"Very low confidence: {confidence}")
        elif confidence < 0.5:
            bottlenecks.append(f"Low confidence: {confidence}")

        # Check for high-risk indicators
        title = task.get("title", "").lower()
        description = task.get("description", "").lower()
        risk_keywords = ["critical", "urgent", "blocker", "security", "vulnerability", "outage"]

        if any(keyword in title or keyword in description for keyword in risk_keywords):
            if score < 5:  # High risk but low score indicates bottleneck
                bottlenecks.append("High-risk task with disproportionately low priority score")

        # Check for resource constraints
        if effort > 5 and task.get("urgency", 0) > 7:
            bottlenecks.append("High urgency task requiring significant effort")

        return bottlenecks

    def is_bottleneck(self, task: TaskData) -> bool:
        """
        Returns True if task is considered a bottleneck.
        """
        return len(self.detect_bottlenecks(task)) > 0

    def explain_bottleneck(self, task: TaskData) -> str:
        """
        Provides explanation for why a task is a bottleneck.
        """
        bottlenecks = self.detect_bottlenecks(task)
        if not bottlenecks:
            return "No bottlenecks detected"

        return "Bottleneck due to: " + ", ".join(bottlenecks)





