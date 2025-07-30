



# analyzers/entity_extractor.py

"""
Entity extraction module for extracting key entities from prepared text.
At MVP level, implements basic structure with expansion capability through external LLMs or specialized NER models.
"""

from typing import List, Dict
import re

class EntityExtractor:
    """
    Basic module for extracting entities from text.
    In MVP version uses simple heuristics/templates.
    Can be replaced with LLM or spaCy in the future.
    """

    def __init__(self):
        # Future: can add model loading or configuration here
        pass

    def extract(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from text.

        :param text: cleaned text
        :return: dictionary with entity types and their values
        """
        # Example: basic template approach
        entities = {
            "dates": self.extract_dates(text),
            "organizations": self.extract_organizations(text),
            "amounts": self.extract_amounts(text),
            "emails": self.extract_emails(text),
            "phones": self.extract_phones(text),
        }

        return entities

    def extract_dates(self, text: str) -> List[str]:
        """Extract date patterns from text."""
        # Date pattern: DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY
        pattern = r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b"
        return re.findall(pattern, text)

    def extract_organizations(self, text: str) -> List[str]:
        """Extract organization names from text."""
        # Placeholder: in the future can use NER or LLM
        # For now, look for common organization indicators
        patterns = [
            r"\b(ООО|ЗАО|ОАО|ПАО|ИП)\s+[\"'‘“]?[А-ЯЁ][а-яё\s\"'‘“-]*[\"'‘”]?",
            r"\b[А-ЯЁ][а-яё\s\"'‘“-]*\s+(Компания|Фирма|Предприятие|Организация)\b"
        ]

        organizations = []
        for pattern in patterns:
            organizations.extend(re.findall(pattern, text))

        return organizations

    def extract_amounts(self, text: str) -> List[str]:
        """Extract monetary amounts from text."""
        # More specific pattern for monetary amounts
        # Look for numbers that are likely to be monetary values
        patterns = [
            # Large amounts (thousands+)
            r"\b\d{1,3}[.,\s]?\d{3}[.,\s]?\d{3}\b",
            # Medium amounts with currency
            r"\b\d{1,3}[.,\s]?\d{3}\s?(₽|руб\.|рублей|USD|долл\.|EUR|евро)?\b",
            # Decimal amounts
            r"\b\d+[.,]\d{2}\s?(₽|руб\.|рублей|USD|долл\.|EUR|евро)?\b",
            # Simple amounts with currency
            r"\b\d+\s(₽|руб\.|рублей|USD|долл\.|EUR|евро)\b",
            # Any 4+ digit number (likely to be monetary)
            r"\b\d{4,}\b"
        ]

        amounts = []
        for pattern in patterns:
            amounts.extend(re.findall(pattern, text))

        # Filter out empty strings and dates
        dates = self.extract_dates(text)
        amounts = [amt for amt in amounts if amt and amt not in dates]

        # Also filter out years (4-digit numbers that are years)
        year_pattern = r"^\d{4}$"
        amounts = [amt for amt in amounts
                  if not (re.match(year_pattern, amt) and 1900 <= int(amt) <= 2100)]

        return amounts

    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text."""
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return re.findall(pattern, text)

    def extract_phones(self, text: str) -> List[str]:
        """Extract phone numbers from text."""
        # Russian phone number patterns
        patterns = [
            r"\b\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}\b",  # +7 (123) 456-78-90
            r"\b\+7\d{10}\b",                        # +71234567890
            r"\b8 \(\d{3}\) \d{3}-\d{2}-\d{2}\b",    # 8 (123) 456-78-90
            r"\b8\d{10}\b",                         # 81234567890
            r"\b\d{3}-\d{2}-\d{2}\b",                # 123-45-67
            r"\b\d{3} \d{3} \d{2} \d{2}\b",          # 123 456 78 90
            r"\b\d{3} \d{2} \d{2}\b"                 # 123 45 67
        ]

        phones = []
        for pattern in patterns:
            phones.extend(re.findall(pattern, text))

        return phones

    def extract_with_spacy(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities using spaCy (future implementation).

        Requires spaCy with ru_core_news_lg model.

        :param text: input text
        :return: dictionary with entity types and values
        """
        try:
            import spacy
            # Load Russian model (would need to be installed)
            nlp = spacy.load("ru_core_news_lg")
            doc = nlp(text)

            entities = {}
            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)

            return entities

        except ImportError:
            # Fallback to basic extraction if spaCy not available
            return self.extract(text)

    def extract_with_llm(self, text: str, prompt: str = None) -> Dict[str, List[str]]:
        """
        Extract entities using LLM (future implementation).

        :param text: input text
        :param prompt: custom prompt for entity extraction
        :return: dictionary with entity types and values
        """
        # Placeholder for LLM integration
        # Would use LangChain or direct API calls
        return {"llm_entities": ["Future implementation"]}



