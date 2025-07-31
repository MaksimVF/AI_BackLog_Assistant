



"""
Domain Router for Second Level Categorization
"""

from .base import BaseContextualCategorizer
from .domains.it import ITCategorizer
from .domains.finance import FinanceCategorizer
from .domains.fallback import FallbackCategorizer

# Registry of domain-specific categorizers
DOMAIN_CATEGORIZERS = {
    "it": ITCategorizer(),
    "finance": FinanceCategorizer(),
    "fallback": FallbackCategorizer()
}

def categorize_document_by_domain(document: str, domain: str) -> dict:
    """
    Routes document to appropriate domain-specific categorizer.

    Args:
        document: The document text to categorize
        domain: The detected domain (e.g., "it", "finance")

    Returns:
        Categorization result
    """
    # Get the appropriate categorizer for the domain
    categorizer = DOMAIN_CATEGORIZERS.get(domain, DOMAIN_CATEGORIZERS["fallback"])

    # Perform categorization
    result = categorizer.categorize(document)

    # Add domain information to result
    result["domain"] = domain

    return result



