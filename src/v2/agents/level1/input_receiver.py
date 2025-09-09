

"""
Input Receiver Agent for Level 1 Processing
"""

from typing import Dict, Any
from pydantic import BaseModel, field_validator
from src.common.utils import sanitize_input
import logging

logger = logging.getLogger(__name__)

class InputData(BaseModel):
    """Input data model with validation"""
    content: str
    source: str = "unknown"
    metadata: Dict[str, Any] = {}

    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Content must not be empty')
        return v

class InputReceiverAgent:
    """Handles receiving and validating input data"""

    def __init__(self):
        self.supported_sources = ["api", "telegram", "email", "web", "integration"]

    def receive(self, raw_data: Dict[str, Any]) -> InputData:
        """
        Receive and validate input data

        Args:
            raw_data: Raw input data from various sources

        Returns:
            Validated InputData object

        Raises:
            ValueError: If input validation fails
        """
        try:
            # Sanitize input
            sanitized_data = sanitize_input(raw_data)

            # Validate source
            source = sanitized_data.get('source', 'unknown')
            if source not in self.supported_sources and source != "unknown":
                logger.warning(f"Unknown source: {source}")

            # Create validated input
            input_data = InputData(
                content=sanitized_data.get('content', ''),
                source=source,
                metadata=sanitized_data.get('metadata', {})
            )

            logger.info(f"Received input from {source}: {len(input_data.content)} characters")
            return input_data

        except Exception as e:
            logger.error(f"Error processing input: {e}")
            raise ValueError(f"Invalid input data: {e}")

    def validate_source(self, source: str) -> bool:
        """Validate if a source is supported"""
        return source in self.supported_sources

