





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
    """

    def __init__(self, score_threshold: float = 3.0):
        self.score_threshold = score_threshold

    def detect_bottlenecks(self, task: TaskData) -> List[str]:
        """
        Detects bottlenecks for a single task.

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

        # Check effort vs impact
        effort = task.get("effort", 1)
        impact = task.get("impact", 1)
        if effort > 0 and impact / effort < 0.5:
            bottlenecks.append(f"High effort relative to impact ({impact}/{effort})")

        # Check dependencies
        if task.get("blocks_count", 0) > 2:
            bottlenecks.append(f"Blocks {task['blocks_count']} other tasks")

        # Check confidence
        confidence = task.get("confidence", 1)
        if confidence < 0.5:
            bottlenecks.append(f"Low confidence: {confidence}")

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





