


"""
Personal Growth Domain Categorizer
"""

import json
import os
from ..base import BaseContextualCategorizer
from ..emb_utils import get_embedding, cosine_similarity

class PersonalGrowthCategorizer(BaseContextualCategorizer):
    """
    Categorizes personal growth-related documents into specific types.
    """

    def __init__(self):
        # Load Personal Growth taxonomy
        current_dir = os.path.dirname(__file__)
        taxonomy_path = os.path.join(current_dir, "taxonomy", "personal_growth_taxonomy.json")

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
                "goal_setting": {"description": "Постановка личных или профессиональных целей"},
                "self_reflection": {"description": "Рефлексия или анализ личного опыта"},
                "learning_plan": {"description": "План обучения или саморазвития"},
                "motivation": {"description": "Мотивационные заметки или цитаты"},
                "habit_tracking": {"description": "Отслеживание привычек или рутины"},
                "personal_challenge": {"description": "Личный вызов или испытание"}
            }
            self.embeddings = {
                category: get_embedding(details["description"])
                for category, details in self.taxonomy.items()
            }

    def categorize(self, document: str) -> dict:
        """
        Categorizes a personal growth document.

        Args:
            document: The document text to categorize

        Returns:
            Categorization result
        """
        if not self.embeddings:
            return {
                "category": "unclassified",
                "confidence": 0.0,
                "source": "personal_growth"
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
            "source": "personal_growth"
        }

# Create singleton instance
categorizer = PersonalGrowthCategorizer()

