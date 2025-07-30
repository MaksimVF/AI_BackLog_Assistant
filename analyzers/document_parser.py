



"""
Document parser module for structural analysis and entity extraction.
This module extracts key entities and structured blocks from document text.
"""

import re
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import logging

# Set up logger
logger = logging.getLogger(__name__)

@dataclass
class ParsedEntity:
    """Represents a parsed entity with its value and position"""
    value: str
    start: int
    end: int
    confidence: float = 1.0

class DocumentParser:
    """
    Base document parser for extracting key entities from text.
    Designed to extract dates, amounts, organization names, contract numbers, etc.
    Ready for extension with spaCy, LLM, or hybrid NER models.
    """

    def __init__(self):
        # Entity patterns
        self.patterns = {
            "inn": r"\b\d{10}\b|\b\d{12}\b",  # Russian INN (10 or 12 digits)
            "date": r"\b\d{2}[./-]\d{2}[./-]\d{4}\b",  # Date formats: DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY
            "sum": r"\b\d{1,3}(?:[ \u00A0]?\d{3})*(?:[.,]\d{2})?\s?(?:₽|руб(?:\.|лей)?)\b",  # Currency amounts
            "org_name": r"(?:ООО|ЗАО|ОАО|ИП)\s+«?[А-ЯA-Z][^»\n]{2,}»?",  # Organization names
            "contract_number": r"№\s?\d{1,10}[-/]*\d{0,10}",  # Contract numbers
            "phone": r"\+?\d[\d -]{8,12}\d",  # Phone numbers
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email addresses
            "fio": r"[А-Я][а-я]+ [А-Я][а-я]+ [А-Я][а-я]+",  # Full name (Russian)
        }

        # Compile regex patterns for better performance
        self.compiled_patterns = {k: re.compile(v, re.IGNORECASE) for k, v in self.patterns.items()}

    def parse(self, text: str) -> Dict[str, Optional[Union[str, List[ParsedEntity]]]]:
        """
        Extract key entities from text.

        Args:
            text: Input document text

        Returns:
            Dictionary with extracted entities and their positions
        """
        if not text:
            return {}

        results = {}

        for entity_type, pattern in self.compiled_patterns.items():
            try:
                # Find all matches for this entity type
                matches = []
                for match in pattern.finditer(text):
                    entity = ParsedEntity(
                        value=match.group(),
                        start=match.start(),
                        end=match.end()
                    )
                    matches.append(entity)

                # Store results (single value for backward compatibility)
                if matches:
                    results[entity_type] = matches[0].value if len(matches) == 1 else matches
                else:
                    results[entity_type] = None

            except Exception as e:
                logger.error(f"Error parsing {entity_type}: {e}")
                results[entity_type] = None

        return results

    def parse_with_details(self, text: str) -> Dict[str, Any]:
        """
        Extract entities with detailed information.

        Args:
            text: Input document text

        Returns:
            Dictionary with detailed entity information
        """
        if not text:
            return {}

        results = {"entities": {}, "metadata": {"text_length": len(text)}}

        for entity_type, pattern in self.compiled_patterns.items():
            try:
                matches = []
                for match in pattern.finditer(text):
                    entity = ParsedEntity(
                        value=match.group(),
                        start=match.start(),
                        end=match.end()
                    )
                    matches.append(entity)

                if matches:
                    results["entities"][entity_type] = {
                        "values": [m.value for m in matches],
                        "positions": [{"start": m.start, "end": m.end} for m in matches],
                        "count": len(matches)
                    }
                else:
                    results["entities"][entity_type] = None

            except Exception as e:
                logger.error(f"Error parsing {entity_type}: {e}")
                results["entities"][entity_type] = None

        return results

    def add_custom_pattern(self, entity_type: str, pattern: str) -> None:
        """
        Add a custom regex pattern for entity extraction.

        Args:
            entity_type: Name of the entity type
            pattern: Regex pattern for the entity
        """
        try:
            compiled = re.compile(pattern, re.IGNORECASE)
            self.compiled_patterns[entity_type] = compiled
            logger.info(f"Added custom pattern for {entity_type}")
        except Exception as e:
            logger.error(f"Invalid pattern for {entity_type}: {e}")

    def extract_structured_blocks(self, text: str) -> Dict[str, Any]:
        """
        Extract structured document blocks (sections, paragraphs, etc.).

        Args:
            text: Input document text

        Returns:
            Dictionary with structured blocks
        """
        # Simple section extraction based on common headers
        sections = {}
        section_patterns = {
            "intro": r"(?:^|\n)(?:Введение|Introduction|Общие положения):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
            "terms": r"(?:^|\n)(?:Условия|Terms|Положения):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
            "payment": r"(?:^|\n)(?:Оплата|Payment|Платежи):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
            "signatures": r"(?:^|\n)(?:Подписи|Signatures|Реквизиты):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
        }

        for section_name, pattern in section_patterns.items():
            try:
                match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                if match:
                    sections[section_name] = match.group(1).strip()
                else:
                    sections[section_name] = None
            except Exception as e:
                logger.error(f"Error extracting {section_name} section: {e}")
                sections[section_name] = None

        return sections

# Example usage
if __name__ == "__main__":
    parser = DocumentParser()

    # Test text
    test_text = """
    Договор № 345/2023 от 01.07.2023 заключён между ООО «Пример» и ИП Иванов.
    Сумма 120 000,00 руб. Срок действия: 1 год.

    Введение
    Настоящий договор регулирует отношения между сторонами.

    Условия
    Оплата производится в течение 30 дней с момента подписания.
    """

    # Basic parsing
    result = parser.parse(test_text)
    print("Basic parsing result:")
    for entity, value in result.items():
        print(f"  {entity}: {value}")

    # Detailed parsing
    detailed = parser.parse_with_details(test_text)
    print("\nDetailed parsing result:")
    print(f"  Text length: {detailed['metadata']['text_length']}")
    for entity, data in detailed['entities'].items():
        if data:
            print(f"  {entity}: {data['values']}")

    # Structured blocks
    blocks = parser.extract_structured_blocks(test_text)
    print("\nStructured blocks:")
    for block, content in blocks.items():
        if content:
            print(f"  {block}: {content[:50]}...")

