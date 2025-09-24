



"""
Prioritization Agent for Level 2 Processing

Enhanced with configuration and error handling.
"""

import logging
from crewai import Agent
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PrioritizationAgent:
    """Prioritizes documents based on content and metadata with enhanced features"""

    def __init__(self, algorithm: str = "default"):
        """
        Initialize PrioritizationAgent with configuration

        Args:
            algorithm: Prioritization algorithm to use
        """
        self.algorithm = algorithm

        # Initialize CrewAI agent
        self.agent = Agent(
            name="PrioritizationAgent",
            role="Агент приоритизации документов",
            goal="""
                Определить приоритет обработки документов на основе их содержания,
                классификации и метаданных.
            """,
            backstory="""
                Ты — агент, отвечающий за определение приоритетов обработки.
                Используешь алгоритмы и правила для оценки важности документов.
            """,
            tools=[],
            verbose=True
        )

    def _calculate_priority(self, classification: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate priority based on classification and metadata

        Args:
            classification: Document classification data
            metadata: Document metadata

        Returns:
            Priority calculation result
        """
        # Default algorithm - can be enhanced with ML models
        base_priority = 0.5

        # Adjust based on classification
        if classification.get("category") == "urgent":
            base_priority += 0.3
        elif classification.get("category") == "important":
            base_priority += 0.2

        # Adjust based on metadata
        if metadata.get("source") == "email":
            base_priority += 0.1

        # Determine priority level
        if base_priority > 0.8:
            priority_level = "high"
        elif base_priority > 0.5:
            priority_level = "medium"
        else:
            priority_level = "low"

        return {
            "priority_level": priority_level,
            "priority_score": base_priority,
            "reason": f"Based on {classification.get('category')} classification and {metadata.get('source')} source"
        }

    def prioritize(self, input_data: dict) -> dict:
        """
        Prioritize document processing with enhanced logic

        Args:
            input_data: Data from Level 1 and categorization

        Returns:
            Data with added prioritization information
        """
        try:
            # Extract required data
            classification = input_data.get("classification", {})
            metadata = input_data.get("metadata", {})

            # Calculate priority
            priority_data = self._calculate_priority(classification, metadata)

            # Add prioritization to data
            prioritized_data = {
                **input_data,
                "prioritization": priority_data
            }

            logger.info(f"Prioritized document {input_data.get('document_id', 'unknown')} as {priority_data['priority_level']}")

            return prioritized_data

        except Exception as e:
            logger.error(f"Prioritization failed: {e}")
            # Add fallback prioritization
            return {
                **input_data,
                "prioritization": {
                    "priority_level": "medium",
                    "priority_score": 0.5,
                    "reason": "fallback prioritization",
                    "error": str(e)
                }
            }


