



"""
Semantic Block Classifier module for categorizing document blocks by content type.
This module analyzes the content of document blocks and assigns semantic categories
to enable targeted processing of different content types.
"""

from typing import List, Dict, Union
import re
import logging

# Set up logger
logger = logging.getLogger(__name__)

class SemanticBlockClassifier:
    """
    Classifies document blocks into semantic categories based on content analysis.
    Uses keyword matching, regex patterns, and can be extended with ML models.
    """

    def __init__(self):
        """
        Initialize the classifier with default category definitions.
        """
        # Define keyword maps for different categories
        self.keywords_map = {
            "financial": {
                "keywords": ["счет", "оплата", "налог", "баланс", "финансовый",
                           "invoice", "payment", "tax", "balance", "financial",
                           "руб", "usd", "eur", "currency", "валюта"],
                "patterns": [r"\b(?:счет|оплата|налог|баланс)\b",
                           r"\b(?:invoice|payment|tax|balance)\b",
                           r"\b\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})\b"]  # Currency amounts
            },
            "legal": {
                "keywords": ["договор", "статья", "суд", "юридический", "соглашение",
                           "contract", "article", "court", "legal", "agreement",
                           "закон", "law", "регламент", "regulation"],
                "patterns": [r"\b(?:договор|соглашение)\b", r"\b(?:contract|agreement)\b",
                           r"\b(?:статья|article)\s+\d+"]  # Article numbers
            },
            "technical": {
                "keywords": ["технический", "инструкция", "параметр", "требование",
                           "technical", "instruction", "parameter", "requirement",
                           "specification", "спецификация", "api", "интерфейс"],
                "patterns": [r"\b(?:технический|инструкция)\b",
                           r"\b(?:technical|instruction)\b",
                           r"\b(?:api|интерфейс)\b"]
            },
            "table": {
                "keywords": ["таблица", "table", "grid", "табличный"],
                "patterns": [r"\|", r"\+\-+", r"\b(?:таблица|table)\b"]  # Markdown and ASCII tables
            },
            "list": {
                "keywords": ["список", "перечень", "list", "перечисление"],
                "patterns": [r"^\s*[-\*\d\.\)]\s+", r"\b(?:список|list)\b"]  # List item patterns
            },
            "metadata": {
                "keywords": ["дата", "date", "автор", "author", "версия", "version"],
                "patterns": [r"\b(?:дата|date):", r"\b(?:автор|author):",
                           r"\b(?:версия|version):"]
            },
            "footer": {
                "keywords": ["страница", "page", "copyright", "©"],
                "patterns": [r"\b(?:страница|page)\s+\d+", r"©\s+\d{4}"]
            }
        }

        # Compile regex patterns
        self.compiled_patterns = {}
        for category, config in self.keywords_map.items():
            self.compiled_patterns[category] = []
            for pattern in config.get("patterns", []):
                try:
                    compiled = re.compile(pattern, re.IGNORECASE)
                    self.compiled_patterns[category].append(compiled)
                except re.error as e:
                    logger.error(f"Invalid pattern in {category}: {e}")

    def add_category(self, category_name: str, keywords: List[str] = None,
                    patterns: List[str] = None) -> None:
        """
        Add a new semantic category.

        Args:
            category_name: Name of the new category
            keywords: List of keywords for this category
            patterns: List of regex patterns for this category
        """
        if category_name in self.keywords_map:
            logger.warning(f"Category {category_name} already exists. Updating.")

        self.keywords_map[category_name] = {
            "keywords": keywords or [],
            "patterns": patterns or []
        }

        # Compile new patterns
        self.compiled_patterns[category_name] = []
        for pattern in patterns or []:
            try:
                compiled = re.compile(pattern, re.IGNORECASE)
                self.compiled_patterns[category_name].append(compiled)
            except re.error as e:
                logger.error(f"Invalid pattern in {category_name}: {e}")

    def classify_blocks(self, blocks: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Classify each block and add a 'category' field.

        Args:
            blocks: List of document blocks from DocumentSchemaGenerator

        Returns:
            List of blocks with added 'category' field
        """
        classified_blocks = []

        for block in blocks:
            classified_block = block.copy()
            content_lower = block["content"].lower()

            # Default category
            classified_block["category"] = "general"
            classified_block["confidence"] = 0.0

            # Check each category
            for category, config in self.keywords_map.items():
                # Check keywords
                keyword_matches = sum(
                    1 for keyword in config.get("keywords", [])
                    if keyword.lower() in content_lower
                )

                # Check patterns
                pattern_matches = sum(
                    1 for pattern in self.compiled_patterns.get(category, [])
                    if pattern.search(block["content"])
                )

                # Calculate confidence score
                confidence = keyword_matches * 0.5 + pattern_matches

                if confidence > classified_block["confidence"]:
                    classified_block["category"] = category
                    classified_block["confidence"] = confidence

            classified_blocks.append(classified_block)

        return classified_blocks

    def classify_with_ml(self, blocks: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Placeholder for ML-based classification.
        Can be extended to use NLP models for better accuracy.

        Args:
            blocks: List of document blocks

        Returns:
            List of blocks with ML-based classification
        """
        # This would be implemented with a real ML model
        logger.info("ML classification not implemented. Using rule-based approach.")
        return self.classify_blocks(blocks)

    def get_category_distribution(self, classified_blocks: List[Dict]) -> Dict[str, int]:
        """
        Get distribution of categories in classified blocks.

        Args:
            classified_blocks: List of classified blocks

        Returns:
            Dictionary with category counts
        """
        distribution = {}
        for block in classified_blocks:
            category = block.get("category", "unknown")
            distribution[category] = distribution.get(category, 0) + 1
        return distribution

# Example usage
if __name__ == "__main__":
    from document_schema import DocumentSchemaGenerator

    # Sample document text
    sample_text = """
    1 Введение
    Это первый абзац документа.

    - Пункт списка 1
    - Пункт списка 2

    | Колонка1 | Колонка2 |
    | -------- | -------- |
    | Значение | Значение |

    2 Основная часть
    Текст основного блока.
    """

    # Generate schema first
    generator = DocumentSchemaGenerator()
    schema = generator.generate_schema(sample_text)

    # Classify blocks
    classifier = SemanticBlockClassifier()
    classified_blocks = classifier.classify_blocks(schema)

    print("Classified Blocks:")
    for block in classified_blocks:
        print(f"{block['type']} ({block['category']}): {block['content'][:30]}...")

    # Get category distribution
    distribution = classifier.get_category_distribution(classified_blocks)
    print("\nCategory Distribution:")
    for category, count in distribution.items():
        print(f"{category}: {count}")



