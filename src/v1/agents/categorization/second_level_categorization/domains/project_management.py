



"""
Project Management Domain Categorizer
"""

import json
import os
from ..base import BaseContextualCategorizer
from ..emb_utils import get_embedding, cosine_similarity

class ProjectManagementCategorizer(BaseContextualCategorizer):
    """
    Categorizes project management-related documents into specific types.
    """

    def __init__(self):
        # Load Project Management taxonomy
        current_dir = os.path.dirname(__file__)
        taxonomy_path = os.path.join(current_dir, "taxonomy", "project_management_taxonomy.json")

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
                "project_plan": {"description": "План проекта или дорожная карта"},
                "task_list": {"description": "Список задач или чеклист"},
                "meeting_notes": {"description": "Заметки или протокол встречи"},
                "risk_assessment": {"description": "Оценка рисков или проблем"},
                "progress_report": {"description": "Отчёт о прогрессе или статусе"},
                "resource_allocation": {"description": "Распределение ресурсов или бюджета"}
            }
            self.embeddings = {
                category: get_embedding(details["description"])
                for category, details in self.taxonomy.items()
            }

    def categorize(self, document: str) -> dict:
        """
        Categorizes a project management document.

        Args:
            document: The document text to categorize

        Returns:
            Categorization result
        """
        if not self.embeddings:
            return {
                "category": "unclassified",
                "confidence": 0.0,
                "source": "project_management"
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
            "source": "project_management"
        }

# Create singleton instance
categorizer = ProjectManagementCategorizer()


