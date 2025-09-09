





"""
Fallback Categorizer
"""

import json
import os
from ..base import BaseContextualCategorizer
from ..emb_utils import get_embedding, cosine_similarity

class FallbackCategorizer(BaseContextualCategorizer):
    """
    Fallback categorizer for documents that don't fit known domains.
    """

    def __init__(self):
        # Load fallback taxonomy
        current_dir = os.path.dirname(__file__)
        taxonomy_path = os.path.join(current_dir, "taxonomy", "fallback_taxonomy.json")

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
                "general_report": {"description": "Общий отчёт или сводка информации"},
                "instruction": {"description": "Инструкция, порядок действий, руководство"},
                "note": {"description": "Примечание, краткая информация или напоминание"},
                "communication": {"description": "Письмо, сообщение, переписка"},
                "unknown": {"description": "Неопознанный документ"}
            }
            self.embeddings = {
                category: get_embedding(details["description"])
                for category, details in self.taxonomy.items()
            }

    def categorize(self, document: str) -> dict:
        """
        Categorizes a document using fallback taxonomy.

        Args:
            document: The document text to categorize

        Returns:
            Categorization result
        """
        if not self.embeddings:
            return {
                "category": "unclassified",
                "confidence": 0.0,
                "source": "fallback"
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

        # Apply confidence threshold
        confidence_threshold = 0.45
        if best_confidence < confidence_threshold:
            best_category = "unknown"

        return {
            "category": best_category,
            "confidence": best_confidence,
            "source": "fallback"
        }

# Create singleton instance
categorizer = FallbackCategorizer()






