
"""
Legal Domain Categorizer
"""

import json
import os
from ..base import BaseContextualCategorizer
from ..emb_utils import get_embedding, cosine_similarity

class LegalCategorizer(BaseContextualCategorizer):
    """
    Categorizes legal-related documents into specific types.
    """

    def __init__(self):
        # Load Legal taxonomy
        current_dir = os.path.dirname(__file__)
        taxonomy_path = os.path.join(current_dir, "taxonomy", "legal_taxonomy.json")

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
                "contract": {"description": "Юридический договор или соглашение"},
                "court_decision": {"description": "Решение суда или арбитража"},
                "legal_opinion": {"description": "Юридическое заключение или мнение"},
                "complaint": {"description": "Жалоба или исковое заявление"},
                "regulation": {"description": "Нормативный акт или постановление"},
                "legal_consultation": {"description": "Запрос на юридическую консультацию"}
            }
            self.embeddings = {
                category: get_embedding(details["description"])
                for category, details in self.taxonomy.items()
            }

    def categorize(self, document: str) -> dict:
        """
        Categorizes a legal document.

        Args:
            document: The document text to categorize

        Returns:
            Categorization result
        """
        if not self.embeddings:
            return {
                "category": "unclassified",
                "confidence": 0.0,
                "source": "legal"
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
            "source": "legal"
        }

# Create singleton instance
categorizer = LegalCategorizer()
