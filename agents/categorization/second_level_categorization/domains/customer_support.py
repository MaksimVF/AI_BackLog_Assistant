


"""
Customer Support Domain Categorizer
"""

import json
import os
from ..base import BaseContextualCategorizer
from ..emb_utils import get_embedding, cosine_similarity

class CustomerSupportCategorizer(BaseContextualCategorizer):
    """
    Categorizes customer support-related documents into specific types.
    """

    def __init__(self):
        # Load Customer Support taxonomy
        current_dir = os.path.dirname(__file__)
        taxonomy_path = os.path.join(current_dir, "taxonomy", "customer_support_taxonomy.json")

        if os.path.exists(taxonomy_path):
            with open(taxonomy_path, "r", encoding="utf-8") as f:
                self.taxonomy = json.load(f)
                # Generate embeddings for category descriptions
                self.embeddings = {
                    category: get_embedding(details["description"])
                    for category, details in self.taxonomy.items()
                }
        else:
            # Default taxonomy if file not found
            self.taxonomy = {
                "technical_issue": {"description": "Техническая проблема или ошибка"},
                "billing_question": {"description": "Вопрос по оплате или счету"},
                "feature_request": {"description": "Запрос на новую функцию или улучшение"},
                "complaint": {"description": "Жалоба на продукт или сервис"},
                "general_question": {"description": "Общий вопрос о продукте или услуге"},
                "account_issue": {"description": "Проблема с аккаунтом или доступом"}
            }
            self.embeddings = {
                category: get_embedding(details["description"])
                for category, details in self.taxonomy.items()
            }

    def categorize(self, document: str) -> dict:
        """
        Categorizes a customer support document.

        Args:
            document: The document text to categorize

        Returns:
            Categorization result
        """
        if not self.embeddings:
            return {
                "category": "unclassified",
                "confidence": 0.0,
                "source": "customer_support"
            }

        # Get document embedding
        doc_emb = get_embedding(document)

        # Compute similarities to all categories
        similarities = {
            category: cosine_similarity(doc_emb, emb)
            for category, emb in self.embeddings.items()
        }

        # Find best match
        best_category, best_confidence = max(similarities.items(), key=lambda x: x[1])

        return {
            "category": best_category,
            "confidence": best_confidence,
            "source": "customer_support"
        }

# Create singleton instance
categorizer = CustomerSupportCategorizer()


