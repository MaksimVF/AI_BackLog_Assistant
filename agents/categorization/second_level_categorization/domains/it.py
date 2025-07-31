




"""
IT Domain Categorizer
"""

import json
import os
from ..base import BaseContextualCategorizer
from ..emb_utils import get_embedding, cosine_similarity

class ITCategorizer(BaseContextualCategorizer):
    """
    Categorizes IT-related documents into specific types.
    """

    def __init__(self):
        # Load IT taxonomy
        current_dir = os.path.dirname(__file__)
        taxonomy_path = os.path.join(current_dir, "taxonomy", "it_taxonomy.json")

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
                "bug_report": {"description": "Описание ошибки или сбоя в системе"},
                "api_specification": {"description": "Описание интерфейса API или контракта взаимодействия"},
                "feature_request": {"description": "Запрос на новую функциональность или изменение"},
                "requirement": {"description": "Формализованные требования к системе или продукту"},
                "deployment_instruction": {"description": "Руководство по развертыванию приложения или сервиса"}
            }
            self.embeddings = {
                category: get_embedding(details["description"])
                for category, details in self.taxonomy.items()
            }

    def categorize(self, document: str) -> dict:
        """
        Categorizes an IT document.

        Args:
            document: The document text to categorize

        Returns:
            Categorization result
        """
        if not self.embeddings:
            return {
                "category": "unclassified",
                "confidence": 0.0,
                "source": "it"
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
            "source": "it"
        }

# Create singleton instance
categorizer = ITCategorizer()




