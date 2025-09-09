



"""
Enhanced Decision Agent with Multiple Sub-Agents
"""

from typing import Dict, Any, List
from .models import TaskData, PriorityResult
from .prioritization_agent import PrioritizationAgent
from .risk_assessment_agent import RiskAssessmentAgent
from .resource_availability_agent import ResourceAvailabilityAgent
from .deadline_sensitivity_agent import DeadlineSensitivityAgent
from .dependency_agent import DependencyAgent
from .user_feedback_agent import UserFeedbackAgent
from .historical_performance_agent import HistoricalPerformanceAgent
from .compliance_agent import ComplianceAgent
from .decision_logic import DecisionLogic
from .recommendation_reporter import RecommendationReporter

class EnhancedDecisionAgent:
    """
    Enhanced Decision Agent that integrates multiple sub-agents to make
    comprehensive decisions about task execution: recommend, postpone, or reject.
    """

    def __init__(self):
        """Initialize with all sub-agents"""
        self.prioritization_agent = PrioritizationAgent()
        self.risk_agent = RiskAssessmentAgent()
        self.resource_agent = ResourceAvailabilityAgent()
        self.deadline_agent = DeadlineSensitivityAgent()
        self.dependency_agent = DependencyAgent()
        self.feedback_agent = UserFeedbackAgent()
        self.history_agent = HistoricalPerformanceAgent()
        self.compliance_agent = ComplianceAgent()
        self.decision_logic = None
        self.recommendation_reporter = RecommendationReporter

    def make_decision(self, task_data: TaskData) -> Dict[str, Any]:
        """
        Make a comprehensive decision about a task using all sub-agents.

        Args:
            task_data: Task data

        Returns:
            Decision result with recommendation and explanation
        """
        # Step 1: Get prioritization results
        priority_result = self.prioritization_agent.prioritize(task_data)

        # Step 2: Run all sub-agents
        risk_assessment = self.risk_agent.assess(task_data)
        resource_assessment = self.resource_agent.assess(task_data)
        deadline_assessment = self.deadline_agent.assess(task_data)
        dependency_assessment = self.dependency_agent.analyze_dependencies(task_data)
        feedback_assessment = self.feedback_agent.analyze_feedback(task_data)
        history_assessment = self.history_agent.analyze_performance(task_data)
        compliance_assessment = self.compliance_agent.check_compliance(task_data)

        # Step 3: Aggregate all factors
        factor_analysis = self._aggregate_factors(
            priority_result,
            risk_assessment,
            resource_assessment,
            deadline_assessment,
            dependency_assessment,
            feedback_assessment,
            history_assessment,
            compliance_assessment
        )

        # Step 4: Make decision based on all factors
        self.decision_logic = DecisionLogic(factor_analysis)
        decision = self.decision_logic.make_decision()

        # Step 5: Generate comprehensive report
        report = self.recommendation_reporter(decision, factor_analysis).generate_report()

        return {
            "decision": decision,
            "report": report,
            "priority_analysis": priority_result,
            "sub_agent_analyses": {
                "risk": risk_assessment,
                "resource": resource_assessment,
                "deadline": deadline_assessment,
                "dependency": dependency_assessment,
                "feedback": feedback_assessment,
                "history": history_assessment,
                "compliance": compliance_assessment
            }
        }

    def _aggregate_factors(self, priority_result: PriorityResult,
                          risk: Dict, resource: Dict, deadline: Dict,
                          dependency: Dict, feedback: Dict,
                          history: Dict, compliance: Dict) -> Dict[str, float]:
        """
        Aggregate factors from all sub-agents into a unified analysis.

        Args:
            priority_result: Results from prioritization
            risk: Risk assessment results
            resource: Resource availability results
            deadline: Deadline sensitivity results
            dependency: Dependency analysis results
            feedback: User feedback analysis results
            history: Historical performance analysis results
            compliance: Compliance check results

        Returns:
            Dictionary of aggregated factors
        """
        # Extract factors from priority result
        score = priority_result.get("score", {}).get("score", 0)
        criticality_map = {"critical": 10, "high": 7, "medium": 5, "low": 2}
        criticality = criticality_map.get(priority_result.get("criticality", "low"), 2)
        effort = priority_result.get("score", {}).get("effort", 1)

        # Map risk to numeric value
        risk_map = {"high": 3, "medium": 2, "low": 1}
        risk_value = risk_map.get(risk.get("risk_label", "low"), 1)

        # Map resource availability to numeric value
        resource_map = {"sufficient": 3, "partial": 2, "insufficient": 1}
        resource_value = resource_map.get(resource.get("resource_label", "insufficient"), 1)

        # Map urgency to numeric value
        urgency_map = {"high": 3, "medium": 2, "low": 1}
        urgency_value = urgency_map.get(deadline.get("urgency_label", "low"), 1)

        # Map dependency severity to numeric value
        dependency_map = {"high": 3, "medium": 2, "low": 1}
        dependency_value = dependency_map.get(dependency.get("dependency_severity", "low"), 1)

        # Map feedback to numeric value
        feedback_map = {"positive": 3, "neutral": 2, "negative": 1}
        feedback_value = feedback_map.get(feedback.get("feedback_label", "neutral"), 2)

        # Map compliance to numeric value
        compliance_map = {"high": 3, "medium": 2, "low": 1}
        compliance_value = compliance_map.get(compliance.get("compliance_level", "low"), 1)

        # Aggregate all factors
        factors = {
            "priority": score,
            "criticality": criticality,
            "effort": effort,
            "risk": risk_value,
            "resource_availability": resource_value,
            "urgency": urgency_value,
            "dependency_severity": dependency_value,
            "user_feedback": feedback_value,
            "compliance": compliance_value,
            "historical_confidence": history.get("historical_success_rate", 0.8)
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



