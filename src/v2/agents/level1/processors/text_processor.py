


"""
Text Processor for Level 1 Processing
"""

import logging
import re
from typing import Dict, Any
from src.v2.agents.level1.input_receiver import InputData

logger = logging.getLogger(__name__)

class TextProcessor:
    """Processes text data for Level 1"""

    def __init__(self):
        # Basic text cleaning patterns
        self.cleaning_patterns = [
            (r'\s+', ' '),  # Multiple spaces to single space
            (r'[^\w\s.,!?;:()-]', ''),  # Remove special characters except basic punctuation
            (r'\n+', ' '),  # Newlines to spaces
            (r'\t+', ' '),  # Tabs to spaces
        ]

    def process(self, input_data: InputData) -> Dict[str, Any]:
        """
        Process text data

        Args:
            input_data: Input data containing text content

        Returns:
            Processed text data with metadata
        """
        try:
            # Clean text
            cleaned_text = self._clean_text(input_data.content)

            # Extract basic metadata
            metadata = {
                'original_length': len(input_data.content),
                'cleaned_length': len(cleaned_text),
                'word_count': len(cleaned_text.split()),
                'source': input_data.source,
                **input_data.metadata
            }

            # Basic sentiment detection (simple heuristic)
            sentiment = self._detect_sentiment(cleaned_text)

            result = {
                'content': cleaned_text,
                'metadata': metadata,
                'sentiment': sentiment
            }

            logger.info(f"Processed text: {len(cleaned_text)} characters, sentiment: {sentiment}")
            return result

        except Exception as e:
            logger.error(f"Error processing text: {e}")
            raise ValueError(f"Text processing failed: {e}")

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        cleaned = text.strip()

        # Apply cleaning patterns
        for pattern, replacement in self.cleaning_patterns:
            cleaned = re.sub(pattern, replacement, cleaned)

        return cleaned.strip()

    def _detect_sentiment(self, text: str) -> str:
        """Basic sentiment detection using simple heuristics"""
        # Simple keyword-based approach
        positive_words = ['good', 'great', 'excellent', 'happy', 'love', 'awesome', 'perfect']
        negative_words = ['bad', 'terrible', 'hate', 'angry', 'problem', 'issue', 'bug', 'error']

        # Count matches
        positive_count = sum(word in text.lower() for word in positive_words)
        negative_count = sum(word in text.lower() for word in negative_words)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'



