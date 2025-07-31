



"""
Domain-specific Categorizers
"""

from .it import ITCategorizer
from .finance import FinanceCategorizer
from .legal import LegalCategorizer
from .healthcare import HealthcareCategorizer
from .personal_growth import PersonalGrowthCategorizer
from .customer_support import CustomerSupportCategorizer
from .project_management import ProjectManagementCategorizer
from .fallback import FallbackCategorizer

# Mapping of domain names to categorizer classes
DOMAIN_CATEGORIZER_CLASSES = {
    "it": ITCategorizer,
    "finance": FinanceCategorizer,
    "legal": LegalCategorizer,
    "healthcare": HealthcareCategorizer,
    "personal_growth": PersonalGrowthCategorizer,
    "customer_support": CustomerSupportCategorizer,
    "project_management": ProjectManagementCategorizer,
    "fallback": FallbackCategorizer
}

def get_categorizer_class(domain: str):
    """
    Gets the categorizer class for a given domain.

    Args:
        domain: The domain name

    Returns:
        Categorizer class or None if not found
    """
    return DOMAIN_CATEGORIZER_CLASSES.get(domain)




