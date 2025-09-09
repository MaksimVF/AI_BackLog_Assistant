




"""
Image Processor for Level 1 Processing with Multiple Providers
"""

import logging
from typing import Dict, Any
from src.v2.agents.level1.processors.base_processor import BaseProcessor
from src.v2.agents.level1.input_receiver import InputData

logger = logging.getLogger(__name__)

class ImageProcessor(BaseProcessor):
    """Processes image data with multiple OCR provider support"""

    def __init__(self):
        super().__init__()
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize available OCR providers"""
        self.available_providers = [
            {
                "name": "tesseract_local",
                "languages": ["en", "ru", "es", "fr", "de", "zh"],
                "requires_internet": False,
                "priority": 1,
                "best_for": ["documents", "printed_text"]
            },
            {
                "name": "paddleocr_local",
                "languages": ["en", "ru", "es", "fr", "de", "zh", "ja", "ko"],
                "requires_internet": False,
                "priority": 2,
                "best_for": ["handwritten", "complex_layouts"]
            },
            {
                "name": "google_vision",
                "languages": ["en", "es", "fr", "de", "ru", "zh", "ja", "ko"],
                "requires_internet": True,
                "priority": 3,
                "best_for": ["handwritten", "complex_images"]
            },
            {
                "name": "yandex_vision",
                "languages": ["ru", "en", "tr"],
                "requires_internet": True,
                "priority": 4,
                "best_for": ["documents", "printed_text"]
            }
        ]

    def _select_provider(self, input_data: Dict[str, Any]) -> str:
        """Select the best OCR provider based on input characteristics"""
        # Get input language and content type if available
        input_language = input_data.metadata.get("language", "en")
        content_type = input_data.metadata.get("content_type", "document")

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

        logger.info(f"Selected OCR provider: {best_provider} for language: {input_language}, content: {content_type}")
        return best_provider

    def _process_with_provider(self, provider_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process image using a specific OCR provider"""
        image_content = input_data.content

        if provider_name == "tesseract_local":
            extracted_text = self._extract_with_tesseract(image_content)
        elif provider_name == "paddleocr_local":
            extracted_text = self._extract_with_paddleocr(image_content)
        elif provider_name == "google_vision":
            extracted_text = self._extract_with_google_vision(image_content)
        elif provider_name == "yandex_vision":
            extracted_text = self._extract_with_yandex_vision(image_content)
        else:
            raise ValueError(f"Unknown provider: {provider_name}")

        return {
            "content": extracted_text,
            "metadata": {
                "original_modality": "image",
                "extraction_length": len(extracted_text),
                "content_type": "extracted_text",
                "provider": provider_name,
                "source": input_data.source,
                **input_data.metadata
            },
            "sentiment": "neutral"  # Placeholder, would be analyzed later
        }

    def _extract_with_tesseract(self, image_data: str) -> str:
        """Extract text using local Tesseract OCR"""
        logger.info("Using Tesseract for OCR")
        return f"[Tesseract] Extracted: {image_data[:50]}..."

    def _extract_with_paddleocr(self, image_data: str) -> str:
        """Extract text using local PaddleOCR"""
        logger.info("Using PaddleOCR for OCR")
        return f"[PaddleOCR] Extracted: {image_data[:50]}..."

    def _extract_with_google_vision(self, image_data: str) -> str:
        """Extract text using Google Vision API"""
        logger.info("Using Google Vision for OCR")
        return f"[Google Vision] Extracted: {image_data[:50]}..."

    def _extract_with_yandex_vision(self, image_data: str) -> str:
        """Extract text using Yandex Vision API"""
        logger.info("Using Yandex Vision for OCR")
        return f"[Yandex Vision] Extracted: {image_data[:50]}..."





