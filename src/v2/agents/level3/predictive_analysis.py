






"""
Predictive Analysis Agent for Level 3 Processing

Provides predictive modeling with:
- Trend prediction
- Future state estimation
- Risk assessment
"""

import logging
from typing import Dict, Any, List
from crewai import Agent

logger = logging.getLogger(__name__)

class PredictiveAnalysisAgent:
    """Performs predictive analysis and modeling"""

    def __init__(self):
        """Initialize PredictiveAnalysisAgent"""
        # Initialize CrewAI agent
        self.agent = Agent(
            name="PredictiveAnalysisAgent",
            role="Агент предиктивного анализа",
            goal="""
                Провести предиктивный анализ для прогнозирования будущих
                состояний, трендов и рисков.
            """,
            backstory="""
                Ты — агент, отвечающий за прогнозирование и анализ будущих состояний.
                Используешь модели машинного обучения и статистические методы.
            """,
            tools=[],
            verbose=True
        )

    def predict_trends(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict future trends

        Args:
            input_data: Data from Level 2 processing

        Returns:
            Data with added trend predictions
        """
        try:
            # Extract required data
            content = input_data.get("content", "")
            classification = input_data.get("classification", {})
            prioritization = input_data.get("prioritization", {})

            # Perform trend prediction
            trend_prediction = {
                "predicted_trends": self._predict_trends(content, classification),
                "trend_confidence": self._calculate_trend_confidence(content),
                "risk_assessment": self._assess_risk(content, classification)
            }

            # Add trend prediction to data
            predicted_data = {
                **input_data,
                "trend_prediction": trend_prediction
            }

            logger.info(f"Trend prediction completed for {input_data.get('document_id', 'unknown')}")

            return predicted_data

        except Exception as e:
            logger.error(f"Trend prediction failed: {e}")
            # Add fallback trend prediction
            return {
                **input_data,
                "trend_prediction": {
                    "predicted_trends": [],
                    "trend_confidence": 0.5,
                    "risk_assessment": "medium",
                    "error": str(e)
                }
            }

    def _predict_trends(self, content: str, classification: Dict[str, Any]) -> List[str]:
        """
        Predict trends based on content and classification

        Args:
            content: Document content
            classification: Document classification

        Returns:
            List of predicted trends
        """
        # Simple trend prediction - can be enhanced with ML models
        trends = []

        # Predict based on classification
        category = classification.get("category", "unknown")
        if category == "urgent":
            trends.append("Increased urgency in similar documents")
        elif category == "important":
            trends.append("More important documents expected")

        # Predict based on content
        if "system" in content.lower():
            trends.append("System-related issues may increase")
        if "user" in content.lower():
            trends.append("User-related topics may trend")

        return trends

    def _calculate_trend_confidence(self, content: str) -> float:
        """
        Calculate trend prediction confidence

        Args:
            content: Document content

        Returns:
            Trend confidence score between 0 and 1
        """
        # Calculate base confidence
        base_confidence = 0.6

        # Adjust based on content length
        if len(content.split()) > 500:
            base_confidence += 0.1
        elif len(content.split()) < 100:
            base_confidence -= 0.1

        # Normalize confidence
        return min(max(base_confidence, 0.1), 1.0)

    def _assess_risk(self, content: str, classification: Dict[str, Any]) -> str:
        """
        Assess risk based on content and classification

        Args:
            content: Document content
            classification: Document classification

        Returns:
            Risk assessment level
        """
        # Simple risk assessment - can be enhanced with risk models
        category = classification.get("category", "unknown")

        if category == "urgent":
            return "high"
        elif category == "important":
            return "medium"
        else:
            return "low"

    def predict_future_state(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict future state

        Args:
            input_data: Data from Level 2 processing

        Returns:
            Future state prediction
        """
        try:
            # Extract required data
            content = input_data.get("content", "")
            classification = input_data.get("classification", {})

            # Perform future state prediction
            future_state = {
                "predicted_state": self._predict_state(content, classification),
                "state_confidence": self._calculate_state_confidence(content),
                "recommended_actions": self._recommend_actions(content, classification)
            }

            # Add future state prediction to data
            predicted_data = {
                **input_data,
                "future_state_prediction": future_state
            }

            logger.info(f"Future state prediction completed for {input_data.get('document_id', 'unknown')}")

            return predicted_data

        except Exception as e:
            logger.error(f"Future state prediction failed: {e}")
            # Add fallback future state prediction
            return {
                **input_data,
                "future_state_prediction": {
                    "predicted_state": "stable",
                    "state_confidence": 0.5,
                    "recommended_actions": [],
                    "error": str(e)
                }
            }

    def _predict_state(self, content: str, classification: Dict[str, Any]) -> str:
        """
        Predict future state

        Args:
            content: Document content
            classification: Document classification

        Returns:
            Predicted future state
        """
        # Simple state prediction - can be enhanced with ML models
        category = classification.get("category", "unknown")

        if category == "urgent":
            return "critical"
        elif category == "important":
            return "stable"
        else:
            return "normal"

    def _calculate_state_confidence(self, content: str) -> float:
        """
        Calculate state prediction confidence

        Args:
            content: Document content

        Returns:
            State confidence score between 0 and 1
        """
        # Calculate base confidence
        base_confidence = 0.6

        # Adjust based on content length
        if len(content.split()) > 500:
            base_confidence += 0.1
        elif len(content.split()) < 100:
            base_confidence -= 0.1

        # Normalize confidence
        return min(max(base_confidence, 0.1), 1.0)

    def _recommend_actions(self, content: str, classification: Dict[str, Any]) -> List[str]:
        """
        Recommend actions based on prediction

        Args:
            content: Document content
            classification: Document classification

        Returns:
            List of recommended actions
        """
        # Simple action recommendation - can be enhanced with decision models
        actions = []

        category = classification.get("category", "unknown")
        if category == "urgent":
            actions.append("Immediate action required")
            actions.append("Notify stakeholders")
        elif category == "important":
            actions.append("Review and prioritize")
            actions.append("Schedule follow-up")

        return actions






