




"""
Reflection Agent for Level 2 Processing

Enhanced with advanced analysis and error handling.
"""

import logging
import re
from crewai import Agent
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ReflectionAgent:
    """Performs reflection analysis on documents with enhanced features"""

    def __init__(self, analysis_level: str = "basic"):
        """
        Initialize ReflectionAgent with configuration

        Args:
            analysis_level: Level of analysis to perform (basic, advanced)
        """
        self.analysis_level = analysis_level

        # Initialize CrewAI agent
        self.agent = Agent(
            name="ReflectionAgent",
            role="Агент рефлексии и анализа документов",
            goal="""
                Провести анализ документов для выявления проблем, противоречий
                и областей для улучшения.
            """,
            backstory="""
                Ты — агент, отвечающий за критический анализ документов.
                Используешь NLP и логический анализ для выявления проблем.
            """,
            tools=[],
            verbose=True
        )

    def _analyze_contradictions(self, content: str) -> List[str]:
        """
        Analyze text for contradictions

        Args:
            content: Document content to analyze

        Returns:
            List of detected contradictions
        """
        # Simple contradiction detection - can be enhanced with NLP
        contradictions = []

        # Check for conflicting statements
        if "but" in content.lower() or "however" in content.lower():
            contradictions.append("Potential contradiction detected in text flow")

        # Check for numerical inconsistencies
        numbers = re.findall(r'\d+', content)
        if len(set(numbers)) < len(numbers):
            contradictions.append("Potential numerical inconsistency detected")

        return contradictions

    def _analyze_quality(self, content: str, classification: Dict[str, Any]) -> float:
        """
        Analyze document quality

        Args:
            content: Document content
            classification: Document classification

        Returns:
            Quality score between 0 and 1
        """
        # Basic quality analysis - can be enhanced with ML models
        base_score = 0.7

        # Adjust based on content length
        if len(content.split()) > 1000:
            base_score += 0.1
        elif len(content.split()) < 100:
            base_score -= 0.1

        # Adjust based on classification
        if classification.get("category") == "urgent":
            base_score += 0.1
        elif classification.get("category") == "unknown":
            base_score -= 0.1

        return min(max(base_score, 0.1), 1.0)

    def analyze(self, input_data: dict) -> dict:
        """
        Perform reflection analysis on document with enhanced logic

        Args:
            input_data: Data from Level 1, categorization, and prioritization

        Returns:
            Data with added reflection analysis
        """
        try:
            # Extract required data
            content = input_data.get("content", "")
            classification = input_data.get("classification", {})
            prioritization = input_data.get("prioritization", {})

            # Perform basic analysis
            contradictions = self._analyze_contradictions(content)
            quality_score = self._analyze_quality(content, classification)

            # Add reflection analysis to data
            analyzed_data = {
                **input_data,
                "reflection": {
                    "issues": ["Basic analysis completed"],
                    "contradictions": contradictions,
                    "improvement_areas": ["Enhance with NLP models"],
                    "quality_score": quality_score,
                    "analysis_level": self.analysis_level
                }
            }

            logger.info(f"Reflection analysis completed for {input_data.get('document_id', 'unknown')} with score {quality_score}")

            return analyzed_data

        except Exception as e:
            logger.error(f"Reflection analysis failed: {e}")
            # Add fallback reflection
            return {
                **input_data,
                "reflection": {
                    "issues": ["Analysis failed"],
                    "contradictions": [],
                    "improvement_areas": [],
                    "quality_score": 0.5,
                    "error": str(e)
                }
            }



