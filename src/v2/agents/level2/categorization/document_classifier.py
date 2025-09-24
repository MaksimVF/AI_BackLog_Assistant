


"""
Document Classifier Agent for Level 2 Processing

Enhanced with machine learning, adaptive learning, and interactive feedback capabilities.
"""

import logging
from functools import lru_cache
from crewai import Agent
from typing import Dict, Any
from src.v2.ml.classification import DocumentClassifierModel
from src.v2.feedback.interactive_agent import InteractiveFeedbackAgent

logger = logging.getLogger(__name__)

class DocumentClassifierAgent:
    """Classifies documents into categories with ML, adaptive learning, and feedback"""

    def __init__(self, cache_size: int = 1000, use_ml: bool = True):
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

        # Initialize ML model
        self.ml_model = DocumentClassifierModel()

        # Initialize feedback agent
        self.feedback_agent = InteractiveFeedbackAgent()

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

    def _classify_with_ml(self, content: str) -> Dict[str, Any]:
        """
        Classify document using machine learning model

        Args:
            content: Document content to classify

        Returns:
            ML-based classification result
        """
        try:
            # Use ML model for classification
            result = self.ml_model.predict(content)

            # Map ML result to standard format
            return {
                "category": result.get("category", "unknown"),
                "domain": "ml_classified",  # Can be enhanced
                "confidence": result.get("confidence", 0.7),
                "ml_model": "document_classifier_v1"
            }

        except Exception as e:
            logger.warning(f"ML classification failed, falling back to agent: {e}")
            # Fall back to agent-based classification
            return self._classify_with_cache(content)

    def classify(self, input_data: dict) -> dict:
        """
        Classify document into categories with ML, adaptive processing, and feedback

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

            # Use ML classification if enabled
            if self.use_ml:
                classification = self._classify_with_ml(content)
            else:
                classification = self._classify_with_cache(content)

            # Add classification to data
            classified_data = {
                **input_data,
                "classification": classification
            }

            # Check if feedback is needed (low confidence)
            if classification.get("confidence", 0) < 0.6:
                # Generate clarifying question
                question = self.feedback_agent.ask_clarifying_question(
                    input_data.get("document_id", "unknown"),
                    classification
                )
                classified_data["feedback_question"] = question

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

    def update_with_feedback(self, document_id: str, correct_category: str):
        """
        Update classification model with user feedback

        Args:
            document_id: ID of the document
            correct_category: Correct classification category
        """
        try:
            # Find document content (simplified - in real implementation, would fetch from storage)
            document_content = f"Sample content for {document_id}"

            # Update ML model
            self.ml_model.update_with_feedback(document_content, correct_category)

            logger.info(f"Updated classification model for {document_id}")

        except Exception as e:
            logger.error(f"Feedback update failed: {e}")
            raise

    def request_feedback(self, document_id: str, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request user feedback on classification

        Args:
            document_id: ID of the document
            classification: Classification result

        Returns:
            Feedback request result
        """
        try:
            # Generate clarifying question
            question = self.feedback_agent.ask_clarifying_question(document_id, classification)

            logger.info(f"Requested feedback for {document_id}")

            return {
                "status": "feedback_requested",
                "question": question
            }

        except Exception as e:
            logger.error(f"Feedback request failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

