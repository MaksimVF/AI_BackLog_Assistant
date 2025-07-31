

"""
Healthcare Domain Categorizer
"""

import json
import os
from ..base import BaseContextualCategorizer
from ..emb_utils import get_embedding, cosine_similarity

class HealthcareCategorizer(BaseContextualCategorizer):
    """
    Categorizes healthcare-related documents into specific types.
    """

    def __init__(self):
        # Load Healthcare taxonomy
        current_dir = os.path.dirname(__file__)
        taxonomy_path = os.path.join(current_dir, "taxonomy", "healthcare_taxonomy.json")

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
                "medical_record": {"description": "Медицинская карта или история болезни"},
                "prescription": {"description": "Рецепт на лекарства"},
                "diagnostic_report": {"description": "Результаты диагностики или анализа"},
                "treatment_plan": {"description": "План лечения или реабилитации"},
                "patient_complaint": {"description": "Жалоба пациента на лечение или обслуживание"},
                "research_paper": {"description": "Научная статья или исследование в медицине"}
            }
            self.embeddings = {
                category: get_embedding(details["description"])
                for category, details in self.taxonomy.items()
            }

    def categorize(self, document: str) -> dict:
        """
        Categorizes a healthcare document.

        Args:
            document: The document text to categorize

        Returns:
            Categorization result
        """
        if not self.embeddings:
            return {
                "category": "unclassified",
                "confidence": 0.0,
                "source": "healthcare"
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
            "source": "healthcare"
        }

# Create singleton instance
categorizer = HealthcareCategorizer()

