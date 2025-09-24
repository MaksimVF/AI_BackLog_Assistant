

"""
Level 2 Processing Pipeline

Coordinates the flow of data through Level 2 agents for:
1. Categorization
2. Prioritization
3. Reflection

Input: Processed data from Level 1
Output: Analyzed and categorized data ready for Level 3
"""

import logging
from typing import Dict, Any
from src.v2.agents.level2.categorization.document_classifier import DocumentClassifierAgent
from src.v2.agents.level2.prioritization.prioritization_agent import PrioritizationAgent
from src.v2.agents.level2.reflection.reflection_agent import ReflectionAgent

logger = logging.getLogger(__name__)

class Level2Pipeline:
    """Coordinates Level 2 processing"""

    def __init__(self):
        # Initialize Level 2 agents
        self.document_classifier = DocumentClassifierAgent()
        self.prioritization_agent = PrioritizationAgent()
        self.reflection_agent = ReflectionAgent()

    def process(self, level1_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through Level 2 pipeline

        Args:
            level1_data: Processed data from Level 1 pipeline

        Returns:
            Analyzed and categorized data
        """
        try:
            # Step 1: Document classification
            logger.info("Level 2: Starting document classification")
            classified_data = self.document_classifier.classify(level1_data)

            # Step 2: Prioritization
            logger.info("Level 2: Starting prioritization")
            prioritized_data = self.prioritization_agent.prioritize(classified_data)

            # Step 3: Reflection
            logger.info("Level 2: Starting reflection analysis")
            reflected_data = self.reflection_agent.analyze(prioritized_data)

            return reflected_data

        except Exception as e:
            logger.error(f"Level 2 processing failed: {e}")
            raise

