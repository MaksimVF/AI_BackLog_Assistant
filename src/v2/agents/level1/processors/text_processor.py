


"""
Text Processor for Level 1 Processing with Multiple Providers
"""

import logging
import re
from typing import Dict, Any
from src.v2.agents.level1.processors.base_processor import BaseProcessor
from src.v2.agents.level1.input_receiver import InputData

logger = logging.getLogger(__name__)

class TextProcessor(BaseProcessor):
    """Processes text data with multiple NLP provider support"""

    def __init__(self):
        super().__init__()
        self._initialize_providers()

        # Basic text cleaning patterns
        self.cleaning_patterns = [
            (r'\s+', ' '),  # Multiple spaces to single space
            (r'[^\w\s.,!?;:()-]', ''),  # Remove special characters except basic punctuation
            (r'\n+', ' '),  # Newlines to spaces
            (r'\t+', ' '),  # Tabs to spaces
        ]

    def _initialize_providers(self):
        """Initialize available text processing providers"""
        self.available_providers = [
            {
                "name": "spacy_local",
                "languages": ["en", "de", "es", "fr", "it", "pt", "nl", "ru"],
                "requires_internet": False,
                "priority": 1,
                "best_for": ["general_text", "named_entity_recognition"]
            },
            {
                "name": "textblob_local",
                "languages": ["en"],
                "requires_internet": False,
                "priority": 2,
                "best_for": ["sentiment_analysis", "simple_text"]
            },
            {
                "name": "google_nlp",
                "languages": ["en", "es", "fr", "de", "ru", "zh", "ja", "ko"],
                "requires_internet": True,
                "priority": 3,
                "best_for": ["complex_analysis", "multilingual"]
            },
            {
                "name": "yandex_nlp",
                "languages": ["ru", "en", "tr"],
                "requires_internet": True,
                "priority": 4,
                "best_for": ["russian_text", "social_media"]
            }
        ]

    def _select_provider(self, input_data: Dict[str, Any]) -> str:
        """Select the best text processing provider based on input characteristics"""
        # Get input language and content type if available
        input_language = input_data.metadata.get("language", "en")
        content_type = input_data.metadata.get("content_type", "general")

        # Filter providers that support the input language
        language_providers = [
            p for p in self.available_providers
            if input_language in p["languages"]
        ]

        if not language_providers:
            # If no providers support the language, use the highest priority one
            return sorted(self.available_providers, key=lambda x: x["priority"])[0]["name"]

        # Filter by content type suitability
        content_providers = [
            p for p in language_providers
            if content_type in p["best_for"]
        ]

        if not content_providers:
            content_providers = language_providers

        # Sort by priority
        best_provider = sorted(content_providers, key=lambda x: x["priority"])[0]["name"]

        logger.info(f"Selected text provider: {best_provider} for language: {input_language}, content: {content_type}")
        return best_provider

    def _process_with_provider(self, provider_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process text using a specific provider"""
        # First clean the text
        cleaned_text = self._clean_text(input_data.content)

        if provider_name == "spacy_local":
            processed_data = self._process_with_spacy(cleaned_text)
        elif provider_name == "textblob_local":
            processed_data = self._process_with_textblob(cleaned_text)
        elif provider_name == "google_nlp":
            processed_data = self._process_with_google_nlp(cleaned_text)
        elif provider_name == "yandex_nlp":
            processed_data = self._process_with_yandex_nlp(cleaned_text)
        else:
            raise ValueError(f"Unknown provider: {provider_name}")

        # Extract basic metadata
        metadata = {
            'original_length': len(input_data.content),
            'cleaned_length': len(cleaned_text),
            'word_count': len(cleaned_text.split()),
            'source': input_data.source,
            'provider': provider_name,
            **processed_data["metadata"],
            **input_data.metadata
        }

        return {
            "content": cleaned_text,
            "metadata": metadata,
            "sentiment": processed_data.get("sentiment", "neutral")
        }

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        cleaned = text.strip()

        # Apply cleaning patterns
        for pattern, replacement in self.cleaning_patterns:
            cleaned = re.sub(pattern, replacement, cleaned)

        return cleaned.strip()

    def _process_with_spacy(self, text_data: str) -> Dict[str, Any]:
        """Process text using local spaCy NLP"""
        logger.info("Using spaCy for text processing")
        # This would perform NER, sentiment analysis, etc.
        return {
            "sentiment": "neutral",  # Placeholder
            "metadata": {
                "entities": ["person1", "organization1"],  # Placeholder
                "language": "en"
            }
        }

    def _process_with_textblob(self, text_data: str) -> Dict[str, Any]:
        """Process text using local TextBlob NLP"""
        logger.info("Using TextBlob for text processing")
        # This would perform sentiment analysis
        return {
            "sentiment": "positive",  # Placeholder
            "metadata": {
                "subjectivity": 0.5,  # Placeholder
                "language": "en"
            }
        }

    def _process_with_google_nlp(self, text_data: str) -> Dict[str, Any]:
        """Process text using Google NLP API"""
        logger.info("Using Google NLP for text processing")
        return {
            "sentiment": "neutral",  # Placeholder
            "metadata": {
                "entities": ["entity1", "entity2"],  # Placeholder
                "language": "en",
                "provider": "google"
            }
        }

    def _process_with_yandex_nlp(self, text_data: str) -> Dict[str, Any]:
        """Process text using Yandex NLP API"""
        logger.info("Using Yandex NLP for text processing")
        return {
            "sentiment": "neutral",  # Placeholder
            "metadata": {
                "entities": ["entity1", "entity2"],  # Placeholder
                "language": "ru",
                "provider": "yandex"
            }
        }



