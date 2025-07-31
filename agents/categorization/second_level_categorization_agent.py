






"""
Second Level Categorization Agent
"""

from .second_level_categorization.domain_router import categorize_document_by_domain

class SecondLevelCategorizationAgent:
    """
    Performs second-level categorization of documents after initial domain detection.

    This agent routes documents to domain-specific categorizers for more granular
    classification within a specific domain.
    """

    def __init__(self):
        pass

    def categorize(self, document: str, domain: str) -> dict:
        """
        Categorizes a document within a specific domain.

        Args:
            document: The document text to categorize
            domain: The detected domain (e.g., "it", "finance")

        Returns:
            Dictionary containing categorization results:
            {
                "domain": str,
                "category": str,
                "confidence": float,
                "source": str
            }
        """
        return categorize_document_by_domain(document, domain)

    def categorize_with_fallback(self, document: str, domain: str) -> dict:
        """
        Categorizes a document with fallback to LLM if confidence is low.

        Args:
            document: The document text to categorize
            domain: The detected domain

        Returns:
            Categorization result
        """
        result = self.categorize(document, domain)

        # If confidence is low, we could fallback to LLM
        # For now, we'll just return the result as-is
        # TODO: Implement LLM fallback logic

        return result





