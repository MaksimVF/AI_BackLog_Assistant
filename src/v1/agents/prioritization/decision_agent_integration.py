

"""
Decision Agent Integration with Prioritization System
"""

from typing import Dict, Any, List
from .models import TaskData, PriorityResult
from .prioritization_agent import PrioritizationAgent
from .decision_logic import DecisionLogic
from .recommendation_reporter import RecommendationReporter
from .factor_analyzer import FactorAnalyzer

class DecisionAgent:
    """
    Decision Agent that integrates with the prioritization system to make
    final decisions about task execution: recommend, postpone, or reject.
    """

    def __init__(self):
        """Initialize with prioritization agent and decision components"""
        self.prioritization_agent = PrioritizationAgent()
        self.factor_analyzer = FactorAnalyzer({})
        self.decision_logic = None
        self.recommendation_reporter = RecommendationReporter

    def make_decision(self, task_data: TaskData) -> Dict[str, Any]:
        """
        Make a decision about a task based on prioritization and other factors.

        Args:
            task_data: Task data

        Returns:
            Decision result with recommendation and explanation
        """
        # Step 1: Get prioritization results
        priority_result = self.prioritization_agent.prioritize(task_data)

        # Step 2: Analyze additional factors
        factor_analysis = self._analyze_factors(priority_result)

        # Step 3: Make decision based on all factors
        self.decision_logic = DecisionLogic(factor_analysis)
        decision = self.decision_logic.make_decision()

        # Step 4: Generate report
        report = self.recommendation_reporter(decision, factor_analysis).generate_report()

        return {
            "decision": decision,
            "report": report,
            "priority_analysis": priority_result
        }

    def _analyze_factors(self, priority_result: PriorityResult) -> Dict[str, float]:
        """
        Analyze factors from prioritization results and other sources.

        Args:
            priority_result: Results from prioritization

        Returns:
            Dictionary of analyzed factors
        """
        # Extract factors from priority result
        score = priority_result.get("score", {}).get("score", 0)
        criticality_map = {"critical": 10, "high": 7, "medium": 5, "low": 2}
        criticality = criticality_map.get(priority_result.get("criticality", "low"), 2)
        effort = priority_result.get("score", {}).get("effort", 1)

        # Additional factors could be analyzed here
        factors = {
            "priority": score,
            "criticality": criticality,
            "effort": effort,
            "risk": 0  # Placeholder for risk analysis
        }

        return factors

    def batch_decision(self, tasks: List[TaskData]) -> List[Dict[str, Any]]:
        """
        Make decisions for a batch of tasks.

        Args:
            tasks: List of task data

        Returns:
            List of decision results
        """
        return [self.make_decision(task) for task in tasks]

