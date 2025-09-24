





"""
Contextual Analysis Agent for Level 3 Processing

Provides advanced contextual analysis with:
- Knowledge graph integration
- Contextual understanding
- Relationship detection
"""

import logging
from typing import Dict, Any, List
from crewai import Agent

logger = logging.getLogger(__name__)

class ContextualAnalysisAgent:
    """Performs advanced contextual analysis"""

    def __init__(self):
        """Initialize ContextualAnalysisAgent"""
        # Initialize CrewAI agent
        self.agent = Agent(
            name="ContextualAnalysisAgent",
            role="Агент контекстного анализа",
            goal="""
                Провести контекстный анализ документов для выявления связей,
                зависимостей и скрытых паттернов.
            """,
            backstory="""
                Ты — агент, отвечающий за глубокий анализ контекста документов.
                Используешь знания о графах и семантические технологии.
            """,
            tools=[],
            verbose=True
        )

    def analyze_context(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform contextual analysis

        Args:
            input_data: Data from Level 2 processing

        Returns:
            Data with added contextual analysis
        """
        try:
            # Extract required data
            content = input_data.get("content", "")
            classification = input_data.get("classification", {})
            prioritization = input_data.get("prioritization", {})

            # Perform basic contextual analysis
            context_analysis = {
                "related_entities": self._extract_entities(content),
                "contextual_relationships": self._detect_relationships(content),
                "contextual_score": self._calculate_contextual_score(content, classification)
            }

            # Add contextual analysis to data
            analyzed_data = {
                **input_data,
                "contextual_analysis": context_analysis
            }

            logger.info(f"Contextual analysis completed for {input_data.get('document_id', 'unknown')}")

            return analyzed_data

        except Exception as e:
            logger.error(f"Contextual analysis failed: {e}")
            # Add fallback contextual analysis
            return {
                **input_data,
                "contextual_analysis": {
                    "related_entities": [],
                    "contextual_relationships": [],
                    "contextual_score": 0.5,
                    "error": str(e)
                }
            }

    def _extract_entities(self, content: str) -> List[str]:
        """
        Extract related entities from content

        Args:
            content: Document content

        Returns:
            List of related entities
        """
        # Simple entity extraction - can be enhanced with NLP
        entities = []

        # Extract common entities
        if "system" in content.lower():
            entities.append("system")
        if "user" in content.lower():
            entities.append("user")
        if "data" in content.lower():
            entities.append("data")

        return entities

    def _detect_relationships(self, content: str) -> List[str]:
        """
        Detect contextual relationships

        Args:
            content: Document content

        Returns:
            List of detected relationships
        """
        # Simple relationship detection - can be enhanced with graph algorithms
        relationships = []

        # Detect common relationships
        if "system" in content.lower() and "user" in content.lower():
            relationships.append("system-user relationship")
        if "data" in content.lower() and "processing" in content.lower():
            relationships.append("data-processing relationship")

        return relationships

    def _calculate_contextual_score(self, content: str, classification: Dict[str, Any]) -> float:
        """
        Calculate contextual score

        Args:
            content: Document content
            classification: Document classification

        Returns:
            Contextual score between 0 and 1
        """
        # Calculate base score
        base_score = 0.5

        # Adjust based on content length
        if len(content.split()) > 500:
            base_score += 0.1
        elif len(content.split()) < 100:
            base_score -= 0.1

        # Adjust based on classification
        if classification.get("category") == "urgent":
            base_score += 0.1
        elif classification.get("category") == "important":
            base_score += 0.05

        # Adjust based on detected relationships
        relationships = self._detect_relationships(content)
        if relationships:
            base_score += 0.1

        # Normalize score
        return min(max(base_score, 0.1), 1.0)

    def analyze_relationships(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze relationships in document

        Args:
            input_data: Data from Level 2 processing

        Returns:
            Relationship analysis result
        """
        try:
            # Extract content
            content = input_data.get("content", "")

            # Detect relationships
            relationships = self._detect_relationships(content)

            # Add relationship analysis
            relationship_analysis = {
                "relationships": relationships,
                "relationship_score": self._calculate_relationship_score(relationships)
            }

            return {
                **input_data,
                "relationship_analysis": relationship_analysis
            }

        except Exception as e:
            logger.error(f"Relationship analysis failed: {e}")
            return {
                **input_data,
                "relationship_analysis": {
                    "relationships": [],
                    "relationship_score": 0.5,
                    "error": str(e)
                }
            }

    def _calculate_relationship_score(self, relationships: List[str]) -> float:
        """
        Calculate relationship score

        Args:
            relationships: Detected relationships

        Returns:
            Relationship score between 0 and 1
        """
        # Base score
        score = 0.5

        # Adjust based on number of relationships
        if len(relationships) > 3:
            score += 0.2
        elif len(relationships) > 1:
            score += 0.1

        return min(max(score, 0.1), 1.0)





