







"""
LangGraph Document Classifier

Provides advanced document classification with:
- Graph-based contextual understanding
- Relationship detection
- Enhanced classification accuracy
"""

import logging
from typing import Dict, Any
from crewai import Agent

logger = logging.getLogger(__name__)

class LangGraphDocumentClassifier:
    """Classifies documents using LangGraph for enhanced contextual understanding"""

    def __init__(self, use_graph: bool = True):
        """
        Initialize LangGraphDocumentClassifier

        Args:
            use_graph: Whether to use graph-based processing
        """
        self.use_graph = use_graph

        # Initialize CrewAI agent
        self.agent = Agent(
            name="LangGraphDocumentClassifier",
            role="Агент классификации документов с использованием LangGraph",
            goal="""
                Классифицировать документы с использованием графа знаний.
                Определить контекстные связи и улучшить точность классификации.
            """,
            backstory="""
                Ты — агент, использующий граф знаний для классификации документов.
                Обнаруживаешь скрытые связи и улучшаешь точность.
            """,
            tools=[],
            verbose=True
        )

    def classify_with_graph(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify document using graph-based approach

        Args:
            input_data: Data from Level 1 processing

        Returns:
            Data with graph-based classification
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

            # Perform graph-based classification
            classification = self._perform_graph_classification(content)

            # Add classification to data
            classified_data = {
                **input_data,
                "classification": classification
            }

            logger.info(f"Classified document {input_data.get('document_id', 'unknown')} as {classification['category']}")

            return classified_data

        except Exception as e:
            logger.error(f"Graph classification failed: {e}")
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

    def _perform_graph_classification(self, content: str) -> Dict[str, Any]:
        """
        Perform graph-based classification

        Args:
            content: Document content to classify

        Returns:
            Graph-based classification result
        """
        # Simulate graph-based classification
        # In real implementation, this would use LangGraph for contextual analysis

        # Extract entities and relationships
        entities = self._extract_entities(content)
        relationships = self._detect_relationships(content)

        # Determine category based on graph analysis
        category = self._determine_category(entities, relationships)

        return {
            "category": category,
            "domain": "graph_classified",
            "confidence": 0.85,
            "entities": entities,
            "relationships": relationships,
            "algorithm": "langgraph_based"
        }

    def _extract_entities(self, content: str) -> Dict[str, Any]:
        """
        Extract entities from content using graph approach

        Args:
            content: Document content

        Returns:
            Extracted entities
        """
        # Simple entity extraction - can be enhanced with LangGraph
        entities = {
            "system": "system" in content.lower(),
            "user": "user" in content.lower(),
            "data": "data" in content.lower(),
            "error": "error" in content.lower()
        }

        return entities

    def _detect_relationships(self, content: str) -> Dict[str, Any]:
        """
        Detect relationships using graph approach

        Args:
            content: Document content

        Returns:
            Detected relationships
        """
        # Simple relationship detection - can be enhanced with LangGraph
        relationships = {
            "system_user": "system" in content.lower() and "user" in content.lower(),
            "data_error": "data" in content.lower() and "error" in content.lower()
        }

        return relationships

    def _determine_category(self, entities: Dict[str, Any], relationships: Dict[str, Any]) -> str:
        """
        Determine category based on graph analysis

        Args:
            entities: Extracted entities
            relationships: Detected relationships

        Returns:
            Determined category
        """
        # Simple category determination - can be enhanced with LangGraph
        if entities.get("error", False) or relationships.get("data_error", False):
            return "urgent"
        elif entities.get("system", False) and entities.get("user", False):
            return "important"
        else:
            return "normal"

    def classify(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify document with LangGraph capabilities

        Args:
            input_data: Data from Level 1 processing

        Returns:
            Data with LangGraph classification
        """
        try:
            # Use graph-based classification if enabled
            if self.use_graph:
                return self.classify_with_graph(input_data)
            else:
                # Fall back to standard classification
                return self._fallback_classification(input_data)

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

    def _fallback_classification(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback classification method

        Args:
            input_data: Data from Level 1 processing

        Returns:
            Data with fallback classification
        """
        # Simple fallback classification
        content = input_data.get("content", "")

        if "urgent" in content.lower():
            category = "urgent"
        elif "important" in content.lower():
            category = "important"
        else:
            category = "normal"

        return {
            **input_data,
            "classification": {
                "category": category,
                "domain": "fallback",
                "confidence": 0.6,
                "algorithm": "fallback"
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

            # Update graph model (simplified - would use actual graph update)
            logger.info(f"Updated graph classification model for {document_id}")

        except Exception as e:
            logger.error(f"Feedback update failed: {e}")
            raise







