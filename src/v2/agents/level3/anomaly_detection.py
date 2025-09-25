







"""
Anomaly Detection Agent for Level 3 Processing

Provides anomaly detection with:
- Pattern recognition
- Outlier detection
- Anomaly scoring
"""

import logging
from typing import Dict, Any, List
from crewai import Agent

logger = logging.getLogger(__name__)

class AnomalyDetectionAgent:
    """Performs anomaly detection and analysis"""

    def __init__(self):
        """Initialize AnomalyDetectionAgent"""
        # Initialize CrewAI agent
        self.agent = Agent(
            name="AnomalyDetectionAgent",
            role="Агент обнаружения аномалий",
            goal="""
                Обнаруживать аномалии и отклонения в документах.
                Выявлять необычные паттерны и потенциальные проблемы.
            """,
            backstory="""
                Ты — агент, отвечающий за обнаружение аномалий.
                Используешь статистические методы и машинное обучение.
            """,
            tools=[],
            verbose=True
        )

    def detect_anomalies(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect anomalies in document

        Args:
            input_data: Data from Level 2 processing

        Returns:
            Data with added anomaly detection
        """
        try:
            # Extract required data
            content = input_data.get("content", "")
            classification = input_data.get("classification", {})
            prioritization = input_data.get("prioritization", {})

            # Perform anomaly detection
            anomaly_detection = {
                "anomalies": self._detect_anomalies(content),
                "anomaly_score": self._calculate_anomaly_score(content),
                "anomaly_type": self._classify_anomaly(content, classification)
            }

            # Add anomaly detection to data
            analyzed_data = {
                **input_data,
                "anomaly_detection": anomaly_detection
            }

            logger.info(f"Anomaly detection completed for {input_data.get('document_id', 'unknown')}")

            return analyzed_data

        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            # Add fallback anomaly detection
            return {
                **input_data,
                "anomaly_detection": {
                    "anomalies": [],
                    "anomaly_score": 0.5,
                    "anomaly_type": "unknown",
                    "error": str(e)
                }
            }

    def _detect_anomalies(self, content: str) -> List[str]:
        """
        Detect anomalies in content

        Args:
            content: Document content

        Returns:
            List of detected anomalies
        """
        # Simple anomaly detection - can be enhanced with ML models
        anomalies = []

        # Detect common anomalies
        if "error" in content.lower():
            anomalies.append("Error pattern detected")
        if "unusual" in content.lower():
            anomalies.append("Unusual pattern detected")
        if "anomaly" in content.lower():
            anomalies.append("Explicit anomaly mentioned")

        return anomalies

    def _calculate_anomaly_score(self, content: str) -> float:
        """
        Calculate anomaly score

        Args:
            content: Document content

        Returns:
            Anomaly score between 0 and 1
        """
        # Calculate base score
        base_score = 0.3

        # Adjust based on detected anomalies
        anomalies = self._detect_anomalies(content)
        if anomalies:
            base_score += 0.2 * len(anomalies)

        # Adjust based on content length
        if len(content.split()) > 1000:
            base_score += 0.1
        elif len(content.split()) < 50:
            base_score -= 0.1

        # Normalize score
        return min(max(base_score, 0.1), 1.0)

    def _classify_anomaly(self, content: str, classification: Dict[str, Any]) -> str:
        """
        Classify anomaly type

        Args:
            content: Document content
            classification: Document classification

        Returns:
            Anomaly type classification
        """
        # Simple anomaly classification - can be enhanced with ML models
        anomalies = self._detect_anomalies(content)
        category = classification.get("category", "unknown")

        if "error" in content.lower() or "Error pattern detected" in anomalies:
            return "error_anomaly"
        elif category == "urgent" and anomalies:
            return "urgent_anomaly"
        elif anomalies:
            return "content_anomaly"
        else:
            return "no_anomaly"

    def analyze_anomaly_patterns(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze anomaly patterns

        Args:
            input_data: Data from Level 2 processing

        Returns:
            Anomaly pattern analysis
        """
        try:
            # Extract content
            content = input_data.get("content", "")

            # Perform pattern analysis
            pattern_analysis = {
                "patterns": self._detect_patterns(content),
                "pattern_score": self._calculate_pattern_score(content),
                "recommended_actions": self._recommend_anomaly_actions(content)
            }

            # Add pattern analysis to data
            analyzed_data = {
                **input_data,
                "anomaly_pattern_analysis": pattern_analysis
            }

            logger.info(f"Anomaly pattern analysis completed for {input_data.get('document_id', 'unknown')}")

            return analyzed_data

        except Exception as e:
            logger.error(f"Anomaly pattern analysis failed: {e}")
            # Add fallback pattern analysis
            return {
                **input_data,
                "anomaly_pattern_analysis": {
                    "patterns": [],
                    "pattern_score": 0.5,
                    "recommended_actions": [],
                    "error": str(e)
                }
            }

    def _detect_patterns(self, content: str) -> List[str]:
        """
        Detect patterns in content

        Args:
            content: Document content

        Returns:
            List of detected patterns
        """
        # Simple pattern detection - can be enhanced with ML models
        patterns = []

        # Detect common patterns
        if "system" in content.lower() and "error" in content.lower():
            patterns.append("system_error_pattern")
        if "user" in content.lower() and "issue" in content.lower():
            patterns.append("user_issue_pattern")

        return patterns

    def _calculate_pattern_score(self, content: str) -> float:
        """
        Calculate pattern score

        Args:
            content: Document content

        Returns:
            Pattern score between 0 and 1
        """
        # Calculate base score
        base_score = 0.4

        # Adjust based on detected patterns
        patterns = self._detect_patterns(content)
        if patterns:
            base_score += 0.1 * len(patterns)

        # Normalize score
        return min(max(base_score, 0.1), 1.0)

    def _recommend_anomaly_actions(self, content: str) -> List[str]:
        """
        Recommend actions for anomalies

        Args:
            content: Document content

        Returns:
            List of recommended actions
        """
        # Simple action recommendation - can be enhanced with decision models
        actions = []

        anomalies = self._detect_anomalies(content)
        if anomalies:
            actions.append("Review detected anomalies")
            actions.append("Investigate root cause")

        return actions






