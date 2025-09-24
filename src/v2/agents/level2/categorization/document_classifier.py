


"""
Document Classifier Agent for Level 2 Processing

Enhanced with caching and configuration support.
"""

import logging
from functools import lru_cache
from crewai import Agent
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DocumentClassifierAgent:
    """Classifies documents into categories with caching and configuration"""

    def __init__(self, cache_size: int = 1000, use_ml: bool = False):
        """
        Initialize DocumentClassifierAgent with configuration options

        Args:
            cache_size: Size of classification cache
            use_ml: Whether to use machine learning for classification
        """
        self.cache_size = cache_size
        self.use_ml = use_ml

        # Initialize CrewAI agent
        self.agent = Agent(
            name="DocumentClassifierAgent",
            role="Агент классификации документов",
            goal="""
                Классифицировать документы по категориям на основе их содержания.
                Определить основную тему, домен и тип документа.
            """,
            backstory="""
                Ты — агент, отвечающий за анализ документов и их классификацию.
                Используешь NLP и машинное обучение для определения категорий.
            """,
            tools=[],
            verbose=True
        )

        # Initialize cache
        self.cache = {}

    @lru_cache(maxsize=1000)
    def _classify_with_cache(self, content: str) -> Dict[str, Any]:
        """
        Classify document content with caching

        Args:
            content: Document content to classify

        Returns:
            Classification result
        """
        # Create minimal input for agent
        minimal_input = {"content": content}

        # Process using CrewAI agent
        result = self.agent.process(minimal_input)

        return {
            "category": result.get("category", "unknown"),
            "domain": result.get("domain", "unknown"),
            "confidence": result.get("confidence", 0.7)
        }

    def classify(self, input_data: dict) -> dict:
        """
        Classify document into categories with enhanced processing

        Args:
            input_data: Data from Level 1 processing

        Returns:
            Data with added classification information
        """
        try:
            # Extract content for classification
            content = input_data.get("content", "")

            if not content:
                logger.warning("Empty content for classification")
                return {
                    **input_data,
                    "classification": {
                        "category": "unknown",
                        "domain": "unknown",
                        "confidence": 0.1
                    }
                }

            # Use cached classification
            classification = self._classify_with_cache(content)

            # Add classification to data
            classified_data = {
                **input_data,
                "classification": classification
            }

            logger.info(f"Classified document {input_data.get('document_id', 'unknown')} as {classification['category']}")

            return classified_data

        except Exception as e:
            logger.error(f"Classification failed: {e}")
            # Add fallback classification
            return {
                **input_data,
                "classification": {
                    "category": "error",
                    "domain": "unknown",
                    "confidence": 0.1,
                    "error": str(e)
                }
            }

