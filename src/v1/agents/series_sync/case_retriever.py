














"""
CaseRetriever for SeriesSync Agent

Finds relevant cases from knowledge base based on similarity.
"""

from typing import Dict, List, Any

class CaseRetriever:
    """
    Retrieves relevant cases from knowledge base using semantic search.
    """

    def __init__(self, case_database: List[Dict[str, Any]]):
        """
        Initialize with case database.

        :param case_database: List of case dictionaries with fields like 'title', 'description', 'tags', 'category'
        """
        self.case_database = case_database

    def find_similar_cases(self, patterns: Dict[str, Any], context: Dict[str, Any], top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Finds most similar cases based on patterns and context.

        :param patterns: Patterns detected by PatternRecognizer
        :param context: Additional context for search
        :param top_k: Number of top results to return
        :return: List of most similar cases
        """
        def similarity_score(case):
            score = 0

            # Match by category
            if case.get("category") == context.get("category"):
                score += 2

            # Match by tags
            common_tags = set(case.get("tags", [])) & set(context.get("tags", []))
            score += len(common_tags)

            # Simple text matching
            if context.get("description"):
                if context["description"][:20] in case.get("description", ""):
                    score += 1

            # Match by detected patterns
            for pattern in patterns.get("patterns_detected", []):
                if isinstance(pattern, str) and pattern.lower() in case.get("description", "").lower():
                    score += 0.5

            return score

        # Sort cases by similarity score
        scored_cases = sorted(
            self.case_database,
            key=lambda c: similarity_score(c),
            reverse=True
        )

        return scored_cases[:top_k]


