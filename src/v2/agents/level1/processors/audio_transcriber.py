



"""
Audio Transcriber for Level 1 Processing with Multiple Providers
"""

import logging
from typing import Dict, Any
from src.v2.agents.level1.processors.base_processor import BaseProcessor
from src.v2.agents.level1.input_receiver import InputData

logger = logging.getLogger(__name__)

class AudioTranscriber(BaseProcessor):
    """Handles audio transcription with multiple provider support"""

    def __init__(self):
        super().__init__()
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize available ASR providers"""
        # List of available providers with their capabilities
        self.available_providers = [
            {
                "name": "whisper_local",
                "languages": ["en", "ru", "es", "fr", "de", "zh"],  # Whisper supports many languages
                "requires_internet": False,
                "priority": 1  # Higher priority for local processing
            },
            {
                "name": "yandex_speechkit",
                "languages": ["ru", "en", "tr"],
                "requires_internet": True,
                "priority": 2
            },
            {
                "name": "google_speech",
                "languages": ["en", "es", "fr", "de", "ru", "zh", "ja", "ko"],
                "requires_internet": True,
                "priority": 3
            }
        ]

    def _select_provider(self, input_data: Dict[str, Any]) -> str:
        """Select the best ASR provider based on input characteristics"""
        # Get input language if available
        input_language = input_data.metadata.get("language", "en")

        # Filter providers that support the input language
        language_providers = [
            p for p in self.available_providers
            if input_language in p["languages"]
        ]

        if not language_providers:
            # If no providers support the language, use the highest priority one
            return sorted(self.available_providers, key=lambda x: x["priority"])[0]["name"]

        # Sort by priority (lower number = higher priority)
        best_provider = sorted(language_providers, key=lambda x: x["priority"])[0]["name"]

        logger.info(f"Selected provider: {best_provider} for language: {input_language}")
        return best_provider

    def _process_with_provider(self, provider_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process audio using a specific ASR provider"""
        audio_content = input_data.content

        if provider_name == "whisper_local":
            transcription = self._transcribe_with_whisper(audio_content)
        elif provider_name == "yandex_speechkit":
            transcription = self._transcribe_with_yandex(audio_content)
        elif provider_name == "google_speech":
            transcription = self._transcribe_with_google(audio_content)
        else:
            raise ValueError(f"Unknown provider: {provider_name}")

        return {
            "content": transcription,
            "metadata": {
                "original_modality": "audio",
                "transcription_length": len(transcription),
                "content_type": "transcription",
                "provider": provider_name,
                "source": input_data.source,
                **input_data.metadata
            },
            "sentiment": "neutral"  # Placeholder, would be analyzed later
        }

    def _transcribe_with_whisper(self, audio_data: str) -> str:
        """Transcribe audio using local Whisper model"""
        # Placeholder for actual Whisper implementation
        # In real implementation, this would use whisper.transcribe()
        logger.info("Using Whisper for local transcription")
        return f"[Whisper] Transcribed: {audio_data[:50]}..."

    def _transcribe_with_yandex(self, audio_data: str) -> str:
        """Transcribe audio using Yandex SpeechKit API"""
        # Placeholder for actual Yandex API implementation
        logger.info("Using Yandex SpeechKit for transcription")
        return f"[Yandex] Transcribed: {audio_data[:50]}..."

    def _transcribe_with_google(self, audio_data: str) -> str:
        """Transcribe audio using Google Speech API"""
        # Placeholder for actual Google API implementation
        logger.info("Using Google Speech for transcription")
        return f"[Google] Transcribed: {audio_data[:50]}..."




