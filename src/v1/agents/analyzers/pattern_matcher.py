

from typing import Dict, List, Optional
from pydantic import BaseModel
from memory.weaviate_client import WeaviateMemory

class PatternAnalysis(BaseModel):
    """Analysis result for pattern matching"""
    is_repeated: bool
    similarity_score: float
    similar_case_id: Optional[str]
    pattern_description: str

class PatternMatcher:
    """Identifies repeating patterns and series in user inputs"""

    def __init__(self, memory: Optional[WeaviateMemory] = None):
        self.memory = memory or WeaviateMemory()

    def analyze_patterns(self, text: str, threshold: float = 0.7) -> PatternAnalysis:
        """
        Analyze text for repeating patterns by comparing with memory

        Args:
            text: Input text to analyze
            threshold: Similarity threshold to consider as a pattern

        Returns:
            PatternAnalysis with pattern matching results
        """
        # Find similar cases
        similar_cases = self.memory.query_similar_cases(text, limit=3)

        if not similar_cases:
            return PatternAnalysis(
                is_repeated=False,
                similarity_score=0.0,
                similar_case_id=None,
                pattern_description="Нет похожих случаев в памяти"
            )

        # For simplicity, we'll use the first case's similarity as representative
        # In a real implementation, we'd calculate proper similarity scores
        similar_case = similar_cases[0]

        # Generate pattern description
        pattern_desc = f"Найден похожий случай: {similar_case['context']} с тегами: {', '.join(similar_case['domain_tags'])}"

        return PatternAnalysis(
            is_repeated=True,
            similarity_score=0.85,  # Placeholder - would be calculated by Weaviate
            similar_case_id=similar_case['id'],
            pattern_description=pattern_desc
        )

