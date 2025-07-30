




import re
from typing import Dict, List, Optional
import logging
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Configure langdetect for better performance
DetectorFactory.seed = 0

class TextCleaner:
    """
    Enhanced text cleaning and normalization module.

    Features:
    - Configurable cleaning options
    - Language detection
    - Multi-language support
    - Trace logging
    - Extensible for tokenization and lemmatization
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize text cleaner with configuration.

        Args:
            config: Dictionary with cleaning options
        """
        self.config = config or {
            "remove_special_chars": True,
            "lowercase": True,
            "remove_extra_spaces": True,
            "detect_language": True,
            "preserve_punctuation": [".", ",", "!", "?", "-"]
        }
        self.logger = logging.getLogger(__name__)

    def clean(self, text: str, log_trace: bool = False) -> Dict:
        """
        Clean and normalize text with comprehensive processing.

        Args:
            text: Input text to clean
            log_trace: Whether to log processing steps

        Returns:
            Dictionary with cleaned text and metadata
        """
        if log_trace:
            self.logger.debug(f"Starting text cleaning: {text[:50]}...")

        # Store original text
        original = text

        # Apply cleaning steps
        if self.config.get("lowercase", True):
            text = text.lower()
            if log_trace:
                self.logger.debug("Applied lowercase conversion")

        if self.config.get("remove_special_chars", True):
            # Preserve specified punctuation
            preserve_chars = "".join(re.escape(c) for c in self.config.get("preserve_punctuation", []))
            pattern = rf"[^\w\s{preserve_chars}]"
            text = re.sub(pattern, "", text)
            if log_trace:
                self.logger.debug(f"Removed special characters, preserved: {self.config.get('preserve_punctuation')}")

        if self.config.get("remove_extra_spaces", True):
            text = re.sub(r"\s+", " ", text).strip()
            if log_trace:
                self.logger.debug("Removed extra whitespace")

        # Detect language
        language = "unknown"
        if self.config.get("detect_language", True):
            try:
                language = detect(text)
                if log_trace:
                    self.logger.debug(f"Detected language: {language}")
            except LangDetectException:
                if log_trace:
                    self.logger.warning("Language detection failed")

        return {
            "original": original,
            "cleaned": text,
            "language": language,
            "length_original": len(original),
            "length_cleaned": len(text),
            "chars_removed": len(original) - len(text)
        }

    def clean_list(self, texts: List[str], log_trace: bool = False) -> List[Dict]:
        """
        Apply cleaning to a list of texts.

        Args:
            texts: List of input texts
            log_trace: Whether to log processing

        Returns:
            List of cleaning results
        """
        return [self.clean(text, log_trace) for text in texts]

    def tokenize(self, text: str) -> List[str]:
        """
        Basic tokenization (can be extended with NLP libraries).

        Args:
            text: Text to tokenize

        Returns:
            List of tokens
        """
        return text.split()

    def normalize_for_language(self, text: str, target_language: str = "ru") -> str:
        """
        Language-specific normalization (placeholder for extension).

        Args:
            text: Text to normalize
            target_language: Target language code

        Returns:
            Normalized text
        """
        # Placeholder for language-specific rules
        if target_language == "ru":
            # Russian-specific normalization rules
            pass
        elif target_language == "en":
            # English-specific normalization rules
            pass
        return text

    def log_processing_trace(self, input_text: str, result: Dict) -> Dict:
        """
        Generate detailed processing trace.

        Args:
            input_text: Original input
            result: Cleaning result

        Returns:
            Trace log dictionary
        """
        return {
            "input": input_text[:100],
            "output": result["cleaned"][:100],
            "language": result["language"],
            "stats": {
                "original_length": result["length_original"],
                "cleaned_length": result["length_cleaned"],
                "chars_removed": result["chars_removed"]
            },
            "config": self.config
        }




