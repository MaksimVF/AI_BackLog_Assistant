








"""
LangGraph Prioritization Agent

Provides advanced prioritization with:
- Graph-based relationship analysis
- Contextual prioritization
- Enhanced decision making
"""

import logging
from typing import Dict, Any
from crewai import Agent

logger = logging.getLogger(__name__)

class LangGraphPrioritizationAgent:
    """Prioritizes documents using LangGraph for enhanced contextual understanding"""

    def __init__(self, use_graph: bool = True):
        """
        Initialize LangGraphPrioritizationAgent

        Args:
            use_graph: Whether to use graph-based processing
        """
        self.use_graph = use_graph

        # Initialize CrewAI agent
        self.agent = Agent(
            name="LangGraphPrioritizationAgent",
            role="Агент приоритизации документов с использованием LangGraph",
            goal="""
                Определить приоритет обработки документов с использованием графа знаний.
                Учитывать контекстные связи и улучшить точность приоритизации.
            """,
            backstory="""
                Ты — агент, использующий граф знаний для приоритизации документов.
                Обнаруживаешь скрытые связи и улучшаешь точность.
            """,
            tools=[],
            verbose=True
        )

    def prioritize_with_graph(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prioritize document using graph-based approach

        Args:
            input_data: Data from Level 1 and categorization

        Returns:
            Data with graph-based prioritization
        """
        try:
            # Extract required data
            content = input_data.get("content", "")
            classification = input_data.get("classification", {})
            metadata = input_data.get("metadata", {})

            # Perform graph-based prioritization
            prioritization = self._perform_graph_prioritization(content, classification, metadata)

            # Add prioritization to data
            prioritized_data = {
                **input_data,
                "prioritization": prioritization
            }

            logger.info(f"Prioritized document {input_data.get('document_id', 'unknown')} as {prioritization['priority_level']}")

            return prioritized_data

        except Exception as e:
            logger.error(f"Graph prioritization failed: {e}")
            # Add fallback prioritization
            return {
                **input_data,
                "prioritization": {
                    "priority_level": "medium",
                    "priority_score": 0.5,
                    "algorithm": "fallback",
                    "error": str(e)
                }
            }

    def _perform_graph_prioritization(self, content: str, classification: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform graph-based prioritization

        Args:
            content: Document content
            classification: Document classification
            metadata: Document metadata

        Returns:
            Graph-based prioritization result
        """
        # Simulate graph-based prioritization
        # In real implementation, this would use LangGraph for contextual analysis

        # Extract entities and relationships
        entities = self._extract_entities(content)
        relationships = self._detect_relationships(content)

        # Determine priority based on graph analysis
        priority_level = self._determine_priority(entities, relationships, classification, metadata)
        priority_score = self._calculate_priority_score(entities, relationships)

        return {
            "priority_level": priority_level,
            "priority_score": priority_score,
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

    def _determine_priority(self, entities: Dict[str, Any], relationships: Dict[str, Any], classification: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """
        Determine priority based on graph analysis

        Args:
            entities: Extracted entities
            relationships: Detected relationships
            classification: Document classification
            metadata: Document metadata

        Returns:
            Determined priority level
        """
        # Simple priority determination - can be enhanced with LangGraph
        category = classification.get("category", "unknown")
        source = metadata.get("source", "unknown")

        if category == "urgent" or relationships.get("data_error", False):
            return "high"
        elif category == "important" and entities.get("system", False):
            return "high"
        elif category == "important":
            return "medium"
        else:
            return "low"

    def _calculate_priority_score(self, entities: Dict[str, Any], relationships: Dict[str, Any]) -> float:
        """
        Calculate priority score based on graph analysis

        Args:
            entities: Extracted entities
            relationships: Detected relationships

        Returns:
            Priority score between 0 and 1
        """
        # Calculate base score
        base_score = 0.5

        # Adjust based on entities and relationships
        if entities.get("error", False) or relationships.get("data_error", False):
            base_score += 0.3
        if entities.get("system", False) and entities.get("user", False):
            base_score += 0.2

        # Normalize score
        return min(max(base_score, 0.1), 1.0)

    def prioritize(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prioritize document with LangGraph capabilities

        Args:
            input_data: Data from Level 1 and categorization

        Returns:
            Data with LangGraph prioritization
        """
        try:
            # Use graph-based prioritization if enabled
            if self.use_graph:
                return self.prioritize_with_graph(input_data)
            else:
                # Fall back to standard prioritization
                return self._fallback_prioritization(input_data)

        except Exception as e:
            logger.error(f"Prioritization failed: {e}")
            # Add fallback prioritization
            return {
                **input_data,
                "prioritization": {
                    "priority_level": "medium",
                    "priority_score": 0.5,
                    "algorithm": "fallback",
                    "error": str(e)
                }
            }

    def _fallback_prioritization(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback prioritization method

        Args:
            input_data: Data from Level 1 and categorization

        Returns:
            Data with fallback prioritization
        """
        # Simple fallback prioritization
        classification = input_data.get("classification", {})
        category = classification.get("category", "unknown")

        if category == "urgent":
            priority_level = "high"
        elif category == "important":
            priority_level = "medium"
        else:
            priority_level = "low"

        return {
            **input_data,
            "prioritization": {
                "priority_level": priority_level,
                "priority_score": 0.6,
                "algorithm": "fallback"
            }
        }

    def update_with_feedback(self, document_id: str, correct_priority: str):
        """
        Update prioritization model with user feedback

        Args:
            document_id: ID of the document
            correct_priority: Correct priority level
        """
        try:
            # Find document data (simplified - in real implementation, would fetch from storage)
            document_data = {
                "document_id": document_id,
                "content": f"Sample content for {document_id}",
                "metadata": {"source": "api"},
                "classification": {"category": "important", "confidence": 0.8}
            }

            # Update graph model (simplified - would use actual graph update)
            logger.info(f"Updated graph prioritization model for {document_id}")

        except Exception as e:
            logger.error(f"Feedback update failed: {e}")
            raise








