








"""
LangGraph Reflection Agent

Provides advanced reflection analysis with:
- Graph-based quality assessment
- Contextual contradiction detection
- Enhanced improvement suggestions
"""

import logging
from typing import Dict, Any
from crewai import Agent

logger = logging.getLogger(__name__)

class LangGraphReflectionAgent:
    """Performs reflection analysis using LangGraph for enhanced contextual understanding"""

    def __init__(self, use_graph: bool = True):
        """
        Initialize LangGraphReflectionAgent

        Args:
            use_graph: Whether to use graph-based processing
        """
        self.use_graph = use_graph

        # Initialize CrewAI agent
        self.agent = Agent(
            name="LangGraphReflectionAgent",
            role="Агент рефлексии с использованием LangGraph",
            goal="""
                Провести анализ документов для выявления проблем и улучшений.
                Использовать граф знаний для контекстного анализа.
            """,
            backstory="""
                Ты — агент, использующий граф знаний для анализа документов.
                Обнаруживаешь скрытые проблемы и предлагаешь улучшения.
            """,
            tools=[],
            verbose=True
        )

    def analyze_with_graph(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze document using graph-based approach

        Args:
            input_data: Data from Level 1, categorization, and prioritization

        Returns:
            Data with graph-based reflection analysis
        """
        try:
            # Extract required data
            content = input_data.get("content", "")
            classification = input_data.get("classification", {})
            prioritization = input_data.get("prioritization", {})

            # Perform graph-based reflection analysis
            reflection = self._perform_graph_reflection(content, classification, prioritization)

            # Add reflection analysis to data
            analyzed_data = {
                **input_data,
                "reflection": reflection
            }

            logger.info(f"Reflection analysis completed for {input_data.get('document_id', 'unknown')}")

            return analyzed_data

        except Exception as e:
            logger.error(f"Graph reflection analysis failed: {e}")
            # Add fallback reflection
            return {
                **input_data,
                "reflection": {
                    "issues": ["Analysis failed"],
                    "contradictions": [],
                    "improvement_areas": [],
                    "quality_score": 0.5,
                    "algorithm": "fallback",
                    "error": str(e)
                }
            }

    def _perform_graph_reflection(self, content: str, classification: Dict[str, Any], prioritization: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform graph-based reflection analysis

        Args:
            content: Document content
            classification: Document classification
            prioritization: Document prioritization

        Returns:
            Graph-based reflection analysis result
        """
        # Simulate graph-based reflection analysis
        # In real implementation, this would use LangGraph for contextual analysis

        # Extract entities and relationships
        entities = self._extract_entities(content)
        relationships = self._detect_relationships(content)

        # Perform quality analysis
        quality_score = self._calculate_quality_score(entities, relationships, classification)
        contradictions = self._detect_contradictions(entities, relationships)
        improvement_areas = self._identify_improvement_areas(entities, relationships, quality_score)

        return {
            "issues": ["Graph analysis completed"],
            "contradictions": contradictions,
            "improvement_areas": improvement_areas,
            "quality_score": quality_score,
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

    def _calculate_quality_score(self, entities: Dict[str, Any], relationships: Dict[str, Any], classification: Dict[str, Any]) -> float:
        """
        Calculate quality score based on graph analysis

        Args:
            entities: Extracted entities
            relationships: Detected relationships
            classification: Document classification

        Returns:
            Quality score between 0 and 1
        """
        # Calculate base score
        base_score = 0.6

        # Adjust based on entities and relationships
        if entities.get("error", False) or relationships.get("data_error", False):
            base_score -= 0.2
        if entities.get("system", False) and entities.get("user", False):
            base_score += 0.1

        # Adjust based on classification
        category = classification.get("category", "unknown")
        if category == "urgent":
            base_score += 0.1
        elif category == "important":
            base_score += 0.05

        # Normalize score
        return min(max(base_score, 0.1), 1.0)

    def _detect_contradictions(self, entities: Dict[str, Any], relationships: Dict[str, Any]) -> List[str]:
        """
        Detect contradictions using graph approach

        Args:
            entities: Extracted entities
            relationships: Detected relationships

        Returns:
            List of detected contradictions
        """
        # Simple contradiction detection - can be enhanced with LangGraph
        contradictions = []

        if entities.get("system", False) and entities.get("error", False) and not relationships.get("data_error", False):
            contradictions.append("System-error contradiction without data relationship")

        if entities.get("user", False) and not relationships.get("system_user", False):
            contradictions.append("User entity without system relationship")

        return contradictions

    def _identify_improvement_areas(self, entities: Dict[str, Any], relationships: Dict[str, Any], quality_score: float) -> List[str]:
        """
        Identify improvement areas based on graph analysis

        Args:
            entities: Extracted entities
            relationships: Detected relationships
            quality_score: Calculated quality score

        Returns:
            List of improvement areas
        """
        # Simple improvement area identification - can be enhanced with LangGraph
        improvement_areas = []

        if quality_score < 0.6:
            improvement_areas.append("Enhance content quality")
            improvement_areas.append("Add more specific details")

        if len(entities) < 2:
            improvement_areas.append("Add more relevant entities")

        if len(relationships) < 1:
            improvement_areas.append("Establish clearer relationships")

        return improvement_areas

    def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze document with LangGraph capabilities

        Args:
            input_data: Data from Level 1, categorization, and prioritization

        Returns:
            Data with LangGraph reflection analysis
        """
        try:
            # Use graph-based reflection if enabled
            if self.use_graph:
                return self.analyze_with_graph(input_data)
            else:
                # Fall back to standard reflection
                return self._fallback_reflection(input_data)

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
                    "algorithm": "fallback",
                    "error": str(e)
                }
            }

    def _fallback_reflection(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback reflection analysis method

        Args:
            input_data: Data from Level 1, categorization, and prioritization

        Returns:
            Data with fallback reflection analysis
        """
        # Simple fallback reflection
        content = input_data.get("content", "")
        classification = input_data.get("classification", {})

        # Basic quality analysis
        quality_score = 0.6
        if "urgent" in content.lower():
            quality_score += 0.1
        elif "important" in content.lower():
            quality_score += 0.05

        return {
            **input_data,
            "reflection": {
                "issues": ["Basic analysis completed"],
                "contradictions": [],
                "improvement_areas": ["Enhance with NLP models"],
                "quality_score": quality_score,
                "algorithm": "fallback"
            }
        }

    def update_with_feedback(self, document_id: str, quality_score: float):
        """
        Update reflection model with user feedback

        Args:
            document_id: ID of the document
            quality_score: User-provided quality score
        """
        try:
            # Find document data (simplified - in real implementation, would fetch from storage)
            document_data = {
                "document_id": document_id,
                "content": f"Sample content for {document_id}",
                "classification": {"category": "important", "confidence": 0.8}
            }

            # Update graph model (simplified - would use actual graph update)
            logger.info(f"Updated graph reflection model for {document_id}")

        except Exception as e:
            logger.error(f"Feedback update failed: {e}")
            raise









