



"""
Document parser module for structural analysis and entity extraction.
This module extracts key entities and structured blocks from document text.
"""

import re
import datetime
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
        # Enhanced entity patterns with improved accuracy
        self.patterns = {
            # Russian INN (10 or 12 digits) with better boundary handling
            "inn": r"(?<!\d)\b\d{10}\b(?!\d)|\b\d{12}\b(?!\d)",

            # Date formats: DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
            "date": r"\b(?:(?:[0-2][0-9]|3[01])[./-](?:0[1-9]|1[0-2])[./-]\d{4}|\d{4}-(?:0[1-9]|1[0-2])-(?:[0-2][0-9]|3[01]))\b",

            # Currency amounts with improved decimal handling
            "sum": r"\b\d{1,3}(?:[ \u00A0]?\d{3})*(?:[.,]\d{1,2})?\s?(?:₽|руб(?:\.|лей)?|USD|EUR|USD|dollars?|euros?)\b",

            # Organization names with better legal form handling
            "org_name": r"(?:ООО|ЗАО|ОАО|ПАО|ИП|АО|ОДО|НП|ГУП|МУП)\s*«?[А-ЯA-Z][^»\n]{2,}»?",

            # Contract numbers with more flexible formats
            "contract_number": r"№\s?\d{1,10}(?:[-/]\d{1,10})*(?:/\d{2,4})?",

            # Phone numbers with international format support
            "phone": r"\+?\d[\d -]{8,14}\d",

            # Email addresses with stricter validation
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",

            # Full name (Russian) with better surname/name/patronymic handling
            "fio": r"(?:[А-Я][а-я]+)\s+(?:[А-Я][а-я]+)\s+(?:[А-Я][а-я]+)",

            # Bank account numbers (Russian format)
            "bank_account": r"\b\d{20}\b",

            # BIC (Bank Identifier Code)
            "bic": r"\b\d{9}\b",

            # KPP (Russian tax code)
            "kpp": r"\b\d{9}\b",

            # OGRN (Russian organization registration number)
            "ogrn": r"\b\d{13}\b",

            # SNILS (Russian insurance number)
            "snils": r"\b\d{3}-\d{3}-\d{3} \d{2}\b",
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

    def extract_structured_blocks(self, text: str, language: str = "ru") -> Dict[str, Any]:
        """
        Extract structured document blocks (sections, paragraphs, etc.).

        Args:
            text: Input document text
            language: Language code for section detection (ru, en, etc.)

        Returns:
            Dictionary with structured blocks
        """
        # Multi-language section patterns
        section_patterns = {}

        if language == "ru":
            section_patterns = {
                "intro": r"(?:^|\n)(?:Введение|Общие положения|Предмет договора):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
                "terms": r"(?:^|\n)(?:Условия|Положения|Обязательства):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
                "payment": r"(?:^|\n)(?:Оплата|Платежи|Финансовые условия):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
                "signatures": r"(?:^|\n)(?:Подписи|Реквизиты|Юридические адреса):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
                "delivery": r"(?:^|\n)(?:Поставка|Доставка|Логистика):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
                "warranty": r"(?:^|\n)(?:Гарантии|Обязательства|Ответственность):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
            }
        elif language == "en":
            section_patterns = {
                "intro": r"(?:^|\n)(?:Introduction|General Provisions|Purpose):?\s*(.*?)(?=\n[A-Z]|$)",
                "terms": r"(?:^|\n)(?:Terms|Conditions|Obligations):?\s*(.*?)(?=\n[A-Z]|$)",
                "payment": r"(?:^|\n)(?:Payment|Financial Terms|Billing):?\s*(.*?)(?=\n[A-Z]|$)",
                "signatures": r"(?:^|\n)(?:Signatures|Legal Addresses|Contact Information):?\s*(.*?)(?=\n[A-Z]|$)",
                "delivery": r"(?:^|\n)(?:Delivery|Shipping|Logistics):?\s*(.*?)(?=\n[A-Z]|$)",
                "warranty": r"(?:^|\n)(?:Warranty|Guarantees|Liability):?\s*(.*?)(?=\n[A-Z]|$)",
            }
        else:
            # Default to Russian if language not supported
            section_patterns = {
                "intro": r"(?:^|\n)(?:Введение|Общие положения|Предмет договора):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
                "terms": r"(?:^|\n)(?:Условия|Положения|Обязательства):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
                "payment": r"(?:^|\n)(?:Оплата|Платежи|Финансовые условия):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
                "signatures": r"(?:^|\n)(?:Подписи|Реквизиты|Юридические адреса):?\s*(.*?)(?=\n[А-ЯA-Z]|$)",
            }

        sections = {}
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

        # Add metadata about the extraction
        sections["_metadata"] = {
            "language": language,
            "sections_found": [k for k, v in sections.items() if v is not None and k != "_metadata"],
            "total_sections": len([k for k, v in sections.items() if k != "_metadata"])
        }

        return sections

    def parse_document(self, text: str, language: str = "ru") -> Dict[str, Any]:
        """
        Comprehensive document parsing that combines entity extraction and structured analysis.

        Args:
            text: Input document text
            language: Language code for section detection

        Returns:
            Dictionary with comprehensive parsing results
        """
        result = {
            "entities": self.parse_with_details(text),
            "structured_blocks": self.extract_structured_blocks(text, language),
            "metadata": {
                "text_length": len(text),
                "language": language,
                "timestamp": datetime.datetime.now().isoformat()
            }
        }

        return result

    def integrate_with_router(self, router_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate document parsing with contextual router results.

        Args:
            router_context: Context from contextual router

        Returns:
            Enhanced context with parsing results
        """
        if not router_context or "text" not in router_context:
            logger.error("Invalid router context for integration")
            return router_context

        # Parse the document
        parsed_results = self.parse_document(router_context["text"])

        # Combine with router context
        enhanced_context = {
            **router_context,
            "parsed_entities": parsed_results["entities"],
            "structured_blocks": parsed_results["structured_blocks"],
            "parsing_metadata": parsed_results["metadata"]
        }

        return enhanced_context

# Example usage
if __name__ == "__main__":
    import datetime

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

    print("=== Document Parser Test ===")

    # Basic parsing
    result = parser.parse(test_text)
    print("\n1. Basic parsing result:")
    for entity, value in result.items():
        if value:
            print(f"  {entity}: {value}")

    # Detailed parsing
    detailed = parser.parse_with_details(test_text)
    print("\n2. Detailed parsing result:")
    print(f"  Text length: {detailed['metadata']['text_length']}")
    for entity, data in detailed['entities'].items():
        if data:
            print(f"  {entity}: {data['values']}")

    # Structured blocks
    blocks = parser.extract_structured_blocks(test_text)
    print("\n3. Structured blocks:")
    for block, content in blocks.items():
        if content and block != "_metadata":
            print(f"  {block}: {content[:50]}...")

    # Comprehensive parsing
    comprehensive = parser.parse_document(test_text)
    print("\n4. Comprehensive parsing metadata:")
    print(f"  Language: {comprehensive['metadata']['language']}")
    print(f"  Sections found: {comprehensive['structured_blocks']['_metadata']['sections_found']}")

    # Example router integration
    router_context = {
        "file_path": "example.txt",
        "file_type": "text",
        "text": test_text,
        "route": "contract_handler"
    }

    enhanced = parser.integrate_with_router(router_context)
    print("\n5. Router integration result:")
    print(f"  Original route: {enhanced['route']}")
    print(f"  Entities found: {len(enhanced['parsed_entities']['entities'])}")
    print(f"  Structured blocks: {len(enhanced['structured_blocks'])}")

