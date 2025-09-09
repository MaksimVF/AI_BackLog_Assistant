


"""
Base Contextual Categorizer
"""

from abc import ABC, abstractmethod

class BaseContextualCategorizer(ABC):
    """
    Base class for domain-specific categorizers.
    """

    @abstractmethod
    def categorize(self, document: str) -> dict:
        """
        Categorizes a document within a specific domain.

        Args:
            document: The document text to categorize

        Returns:
            Dictionary containing:
            {
                "category": str,      # The detected category
                "confidence": float,  # Confidence score (0-1)
                "source": str         # Source of categorization (embedding, llm, etc.)
            }
        """
        pass


