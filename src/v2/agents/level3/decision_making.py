








"""
Advanced Decision Making Agent for Level 3 Processing

Provides advanced decision making with:
- Multi-criteria decision analysis
- Risk-based decision making
- Optimization algorithms
"""

import logging
from typing import Dict, Any, List
from crewai import Agent

logger = logging.getLogger(__name__)

class AdvancedDecisionAgent:
    """Performs advanced decision making and optimization"""

    def __init__(self):
        """Initialize AdvancedDecisionAgent"""
        # Initialize CrewAI agent
        self.agent = Agent(
            name="AdvancedDecisionAgent",
            role="Агент принятия решений",
            goal="""
                Принимать сложные решения на основе анализа данных,
                рисков и приоритетов.
            """,
            backstory="""
                Ты — агент, отвечающий за принятие решений.
                Используешь алгоритмы оптимизации и многокритериальный анализ.
            """,
            tools=[],
            verbose=True
        )

    def make_decision(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make advanced decision based on analysis

        Args:
            input_data: Data from Level 2 and Level 3 processing

        Returns:
            Data with added decision information
        """
        try:
            # Extract required data
            content = input_data.get("content", "")
            classification = input_data.get("classification", {})
            prioritization = input_data.get("prioritization", {})
            contextual_analysis = input_data.get("contextual_analysis", {})
            trend_prediction = input_data.get("trend_prediction", {})
            anomaly_detection = input_data.get("anomaly_detection", {})

            # Perform decision making
            decision = {
                "decision": self._make_decision(content, classification, prioritization),
                "decision_confidence": self._calculate_decision_confidence(content, classification),
                "recommended_actions": self._recommend_actions(content, classification, prioritization),
                "risk_assessment": self._assess_risk(content, classification, anomaly_detection)
            }

            # Add decision to data
            decided_data = {
                **input_data,
                "decision": decision
            }

            logger.info(f"Decision made for {input_data.get('document_id', 'unknown')}")

            return decided_data

        except Exception as e:
            logger.error(f"Decision making failed: {e}")
            # Add fallback decision
            return {
                **input_data,
                "decision": {
                    "decision": "review_required",
                    "decision_confidence": 0.5,
                    "recommended_actions": [],
                    "risk_assessment": "medium",
                    "error": str(e)
                }
            }

    def _make_decision(self, content: str, classification: Dict[str, Any], prioritization: Dict[str, Any]) -> str:
        """
        Make decision based on analysis

        Args:
            content: Document content
            classification: Document classification
            prioritization: Document prioritization

        Returns:
            Decision result
        """
        # Simple decision making - can be enhanced with optimization algorithms
        category = classification.get("category", "unknown")
        priority = prioritization.get("priority_level", "medium")

        if category == "urgent" and priority == "high":
            return "immediate_action"
        elif category == "important" and priority == "high":
            return "priority_action"
        elif category == "urgent" and priority == "medium":
            return "review_required"
        else:
            return "routine_processing"

    def _calculate_decision_confidence(self, content: str, classification: Dict[str, Any]) -> float:
        """
        Calculate decision confidence

        Args:
            content: Document content
            classification: Document classification

        Returns:
            Decision confidence score between 0 and 1
        """
        # Calculate base confidence
        base_confidence = 0.6

        # Adjust based on classification
        category = classification.get("category", "unknown")
        if category == "urgent":
            base_confidence += 0.2
        elif category == "important":
            base_confidence += 0.1

        # Adjust based on content length
        if len(content.split()) > 500:
            base_confidence += 0.1
        elif len(content.split()) < 100:
            base_confidence -= 0.1

        # Normalize confidence
        return min(max(base_confidence, 0.1), 1.0)

    def _recommend_actions(self, content: str, classification: Dict[str, Any], prioritization: Dict[str, Any]) -> List[str]:
        """
        Recommend actions based on decision

        Args:
            content: Document content
            classification: Document classification
            prioritization: Document prioritization

        Returns:
            List of recommended actions
        """
        # Simple action recommendation - can be enhanced with decision models
        actions = []

        category = classification.get("category", "unknown")
        priority = prioritization.get("priority_level", "medium")

        if category == "urgent" and priority == "high":
            actions.append("Immediate action required")
            actions.append("Notify stakeholders")
            actions.append("Escalate to management")
        elif category == "important" and priority == "high":
            actions.append("Priority processing")
            actions.append("Schedule follow-up")
            actions.append("Monitor progress")

        return actions

    def _assess_risk(self, content: str, classification: Dict[str, Any], anomaly_detection: Dict[str, Any]) -> str:
        """
        Assess risk based on analysis

        Args:
            content: Document content
            classification: Document classification
            anomaly_detection: Anomaly detection result

        Returns:
            Risk assessment level
        """
        # Simple risk assessment - can be enhanced with risk models
        category = classification.get("category", "unknown")
        anomaly_score = anomaly_detection.get("anomaly_score", 0.5)

        if category == "urgent" and anomaly_score > 0.7:
            return "high"
        elif category == "urgent" or anomaly_score > 0.7:
            return "medium"
        else:
            return "low"

    def optimize_processing(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize processing based on decision

        Args:
            input_data: Data from Level 2 and Level 3 processing

        Returns:
            Optimization result
        """
        try:
            # Extract required data
            content = input_data.get("content", "")
            classification = input_data.get("classification", {})
            prioritization = input_data.get("prioritization", {})

            # Perform optimization
            optimization = {
                "optimized_processing": self._optimize_processing(content, classification, prioritization),
                "optimization_score": self._calculate_optimization_score(content, classification),
                "resource_allocation": self._allocate_resources(content, classification, prioritization)
            }

            # Add optimization to data
            optimized_data = {
                **input_data,
                "optimization": optimization
            }

            logger.info(f"Processing optimized for {input_data.get('document_id', 'unknown')}")

            return optimized_data

        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            # Add fallback optimization
            return {
                **input_data,
                "optimization": {
                    "optimized_processing": "standard",
                    "optimization_score": 0.5,
                    "resource_allocation": "default",
                    "error": str(e)
                }
            }

    def _optimize_processing(self, content: str, classification: Dict[str, Any], prioritization: Dict[str, Any]) -> str:
        """
        Optimize processing based on analysis

        Args:
            content: Document content
            classification: Document classification
            prioritization: Document prioritization

        Returns:
            Optimized processing type
        """
        # Simple optimization - can be enhanced with optimization algorithms
        category = classification.get("category", "unknown")
        priority = prioritization.get("priority_level", "medium")

        if category == "urgent" and priority == "high":
            return "fast_track"
        elif category == "important" and priority == "high":
            return "priority_queue"
        else:
            return "standard_processing"

    def _calculate_optimization_score(self, content: str, classification: Dict[str, Any]) -> float:
        """
        Calculate optimization score

        Args:
            content: Document content
            classification: Document classification

        Returns:
            Optimization score between 0 and 1
        """
        # Calculate base score
        base_score = 0.6

        # Adjust based on classification
        category = classification.get("category", "unknown")
        if category == "urgent":
            base_score += 0.2
        elif category == "important":
            base_score += 0.1

        # Normalize score
        return min(max(base_score, 0.1), 1.0)

    def _allocate_resources(self, content: str, classification: Dict[str, Any], prioritization: Dict[str, Any]) -> str:
        """
        Allocate resources based on optimization

        Args:
            content: Document content
            classification: Document classification
            prioritization: Document prioritization

        Returns:
            Resource allocation recommendation
        """
        # Simple resource allocation - can be enhanced with optimization algorithms
        category = classification.get("category", "unknown")
        priority = prioritization.get("priority_level", "medium")

        if category == "urgent" and priority == "high":
            return "high_priority_resources"
        elif category == "important" and priority == "high":
            return "medium_priority_resources"
        else:
            return "standard_resources"







