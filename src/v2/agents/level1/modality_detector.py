


"""
Modality Detection Agent for Level 1 Processing
"""

import logging
import mimetypes
from typing import Dict, Any
from src.v2.agents.level1.input_receiver import InputData

logger = logging.getLogger(__name__)

class ModalityDetectionAgent:
    """Detects the modality of input data"""

    def __init__(self):
        self.supported_modalities = ["text", "audio", "video", "image", "document"]

        # Initialize detection providers
        self.providers = [
            {
                "name": "mimetypes_local",
                "priority": 1,
                "requires_internet": False
            },
            {
                "name": "file_magic_local",
                "priority": 2,
                "requires_internet": False
            },
            {
                "name": "google_drive_api",
                "priority": 3,
                "requires_internet": True
            }
        ]

    def detect(self, input_data: InputData) -> str:
        """
        Detect the modality of input data using multiple detection methods

        Args:
            input_data: Validated input data

        Returns:
            Detected modality

        Raises:
            ValueError: If modality cannot be determined
        """
        try:
            # First check if content is direct text (fastest method)
            if self._is_text_content(input_data.content):
                logger.info("Detected modality: text (direct content)")
                return "text"

            # Try each detection method in priority order
            for provider in sorted(self.providers, key=lambda x: x["priority"]):
                try:
                    if provider["name"] == "mimetypes_local":
                        modality = self._detect_with_mimetypes(input_data)
                    elif provider["name"] == "file_magic_local":
                        modality = self._detect_with_file_magic(input_data)
                    elif provider["name"] == "google_drive_api":
                        modality = self._detect_with_google_drive(input_data)
                    else:
                        continue

                    if modality and self.validate_modality(modality):
                        logger.info(f"Detected modality: {modality} using {provider['name']}")
                        return modality

                except Exception as provider_error:
                    logger.warning(f"Detection method {provider['name']} failed: {provider_error}")
                    continue

            # If all methods fail, use fallback
            logger.warning("All detection methods failed, using fallback")
            return self._fallback_detection(input_data)

        except Exception as e:
            logger.error(f"Error detecting modality: {e}")
            raise ValueError(f"Could not determine modality: {e}")

    def _detect_with_mimetypes(self, input_data: InputData) -> str:
        """Detect modality using MIME types"""
        # Try to detect from file extension or content
        if input_data.metadata.get("file_path"):
            mime_type, _ = mimetypes.guess_type(input_data.metadata["file_path"])
            return self._mime_to_modality(mime_type)

        # Try to detect from content if it's a URL or file path
        content = input_data.content
        if content.startswith(("http://", "https://")):
            # For URLs, we might need to fetch headers (not implemented here)
            return "text"  # Default for URLs
        else:
            # Try to guess from content
            mime_type, _ = mimetypes.guess_type(content)
            return self._mime_to_modality(mime_type)

    def _detect_with_file_magic(self, input_data: InputData) -> str:
        """Detect modality using file magic numbers (placeholder)"""
        # This would use python-magic or similar library
        # For now, fallback to mimetypes
        return self._detect_with_mimetypes(input_data)

    def _detect_with_google_drive(self, input_data: InputData) -> str:
        """Detect modality using Google Drive API (placeholder)"""
        # This would use Google Drive API to analyze the file
        # For now, fallback to mimetypes
        return self._detect_with_mimetypes(input_data)

    def _mime_to_modality(self, mime_type: str) -> str:
        """Convert MIME type to modality"""
        if not mime_type:
            return "text"  # Default

        if mime_type.startswith("audio/"):
            return "audio"
        elif mime_type.startswith("video/"):
            return "video"
        elif mime_type.startswith("image/"):
            return "image"
        elif mime_type.startswith("text/") or "json" in mime_type:
            return "text"
        elif mime_type in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return "document"
        else:
            return "text"  # Default to text for unknown types

    def _fallback_detection(self, input_data: InputData) -> str:
        """Fallback detection method"""
        # Check metadata for hints
        if input_data.metadata.get("file_type"):
            file_type = input_data.metadata["file_type"].lower()

            if file_type.startswith("audio/"):
                return "audio"
            elif file_type.startswith("video/"):
                return "video"
            elif file_type.startswith("image/"):
                return "image"
            elif file_type in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                return "document"

        # Check file extension if available
        if input_data.metadata.get("file_name"):
            file_extension = input_data.metadata["file_name"].split(".")[-1].lower()

            audio_extensions = ["mp3", "wav", "ogg", "flac"]
            video_extensions = ["mp4", "avi", "mov", "mkv"]
            image_extensions = ["jpg", "jpeg", "png", "gif", "bmp"]
            document_extensions = ["pdf", "doc", "docx", "txt"]

            if file_extension in audio_extensions:
                return "audio"
            elif file_extension in video_extensions:
                return "video"
            elif file_extension in image_extensions:
                return "image"
            elif file_extension in document_extensions:
                return "document"

        # Default to text
        return "text"

    def _is_text_content(self, content: str) -> bool:
        """Check if content appears to be direct text"""
        # Simple heuristic: if content is reasonably long and contains multiple words
        if len(content) > 50 and len(content.split()) > 5:
            return True
        return False

    def validate_modality(self, modality: str) -> bool:
        """Validate if a modality is supported"""
        return modality in self.supported_modalities


