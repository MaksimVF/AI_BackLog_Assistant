


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

    def detect(self, input_data: InputData) -> str:
        """
        Detect the modality of input data

        Args:
            input_data: Validated input data

        Returns:
            Detected modality

        Raises:
            ValueError: If modality cannot be determined
        """
        try:
            # Check if content is direct text
            if self._is_text_content(input_data.content):
                return "text"

            # Check metadata for file information
            if input_data.metadata.get('file_type'):
                file_type = input_data.metadata['file_type'].lower()

                if file_type.startswith('audio/'):
                    return "audio"
                elif file_type.startswith('video/'):
                    return "video"
                elif file_type.startswith('image/'):
                    return "image"
                elif file_type in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                    return "document"

            # Check file extension if available
            if input_data.metadata.get('file_name'):
                file_extension = input_data.metadata['file_name'].split('.')[-1].lower()

                audio_extensions = ['mp3', 'wav', 'ogg', 'flac']
                video_extensions = ['mp4', 'avi', 'mov', 'mkv']
                image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
                document_extensions = ['pdf', 'doc', 'docx', 'txt']

                if file_extension in audio_extensions:
                    return "audio"
                elif file_extension in video_extensions:
                    return "video"
                elif file_extension in image_extensions:
                    return "image"
                elif file_extension in document_extensions:
                    return "document"

            # Default to text if no clear modality detected
            logger.warning(f"Could not determine modality for input, defaulting to text")
            return "text"

        except Exception as e:
            logger.error(f"Error detecting modality: {e}")
            raise ValueError(f"Could not determine modality: {e}")

    def _is_text_content(self, content: str) -> bool:
        """Check if content appears to be direct text"""
        # Simple heuristic: if content is reasonably long and contains multiple words
        if len(content) > 50 and len(content.split()) > 5:
            return True
        return False

    def validate_modality(self, modality: str) -> bool:
        """Validate if a modality is supported"""
        return modality in self.supported_modalities


