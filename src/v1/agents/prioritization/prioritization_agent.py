







"""
Main Prioritization Agent
"""

from typing import Dict, List
from datetime import datetime
from .models import TaskData, PriorityResult
from .scoring_agent import ScoringAgent
from .bottleneck_detector import BottleneckDetectorAgent
from .criticality_classifier import CriticalityClassifierAgent
from .effort_estimator import EffortEstimatorAgent

class PrioritizationAgent:
    """
    Main agent for task prioritization.
    Combines scoring, bottleneck detection, and criticality classification.
    """

    def __init__(self, llm_client=None):
        """
        Initialize with optional LLM client for enhanced estimation.

        Args:
            llm_client: Optional LLM client for better parameter estimation
        """
        self.scorer = ScoringAgent()
        self.bottleneck_detector = BottleneckDetectorAgent()
        self.criticality_classifier = CriticalityClassifierAgent()
        self.effort_estimator = EffortEstimatorAgent(llm_client)

    def prioritize(self, task: TaskData) -> PriorityResult:
        """
        Prioritizes a task and returns comprehensive analysis.

        Args:
            task: Task data

        Returns:
            PriorityResult with all analysis
        """
        # Ensure all required parameters are present
        if task.get("effort") is None:
            task["effort"] = self.effort_estimator.estimate_effort(task)

        if task.get("impact") is None:
            task["impact"] = self.effort_estimator.estimate_impact(task)

        if task.get("confidence") is None:
            task["confidence"] = self.effort_estimator.estimate_confidence(task)

        # Calculate score
        score = self.scorer.score_task(task)
        task["score"] = score  # Add score to task for bottleneck detection

        # Determine criticality
        criticality = self.criticality_classifier.classify(task)

        # Detect bottlenecks
        bottlenecks = self.bottleneck_detector.detect_bottlenecks(task)
        is_bottleneck = len(bottlenecks) > 0

        # Generate reasoning
        reasoning = [
            f"Impact: {task['impact']}",
            f"Confidence: {task['confidence']}",
            f"Effort: {task['effort']}"
        ]

        if score.get("reach"):
            reasoning.append(f"Reach: {score['reach']}")

        if task.get("urgency"):
            reasoning.append(f"Urgency: {task['urgency']}")

        if task.get("is_blocking"):
            reasoning.append("Blocks other tasks")

        if task.get("is_dependency"):
            reasoning.append("Has dependencies")

        # Add criticality reasoning
        reasoning.append(self.criticality_classifier.explain(task))

        # Create result
        result: PriorityResult = {
            "task_id": task.get("task_id", ""),
            "score": score,
            "criticality": criticality,
            "is_bottleneck": is_bottleneck,
            "bottlenecks": bottlenecks,
            "reasoning": reasoning,
            "explanation": f"Priority: {criticality}, Score: {score['score']}",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        return result

    def batch_prioritize(self, tasks: List[TaskData]) -> List[PriorityResult]:
        """
        Prioritizes multiple tasks.

        Args:
            tasks: List of task data

        Returns:
            List of PriorityResult
        """
        return [self.prioritize(task) for task in tasks]

    def configure_thresholds(self, critical_threshold: float = 8.0, high_threshold: float = 6.0, medium_threshold: float = 4.0):
        """
        Configure criticality thresholds.

        Args:
            critical_threshold: Minimum score for critical classification
            high_threshold: Minimum score for high classification
            medium_threshold: Minimum score for medium classification
        """
        self.criticality_classifier = CriticalityClassifierAgent(
            critical_threshold=critical_threshold,
            high_threshold=high_threshold,
            medium_threshold=medium_threshold
        )

    def configure_bottleneck_thresholds(self, score_threshold: float = 3.0, effort_impact_ratio: float = 0.5):
        """
        Configure bottleneck detection thresholds.

        Args:
            score_threshold: Minimum score to avoid bottleneck classification
            effort_impact_ratio: Minimum acceptable impact/effort ratio
        """
        self.bottleneck_detector = BottleneckDetectorAgent(
            score_threshold=score_threshold,
            effort_impact_ratio=effort_impact_ratio
        )





