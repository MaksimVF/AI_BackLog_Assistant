


"""
Text cleaning utilities for document processing.
"""

import re
import logging
from typing import Optional

def clean_text(file_path: str) -> str:
    """
    Clean text from a document file.

    Args:
        file_path: Path to the document file

    Returns:
        Cleaned text content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic text cleaning
        cleaned = re.sub(r'\s+', ' ', content)  # Normalize whitespace
        cleaned = re.sub(r'[^\w\s.,;:!?-]', '', cleaned)  # Remove special chars
        return cleaned.strip()

    except Exception as e:
        logging.error(f"Error cleaning text from {file_path}: {e}")
        return ""

def clean_text_content(text: str) -> str:
    """
    Clean text content directly.

    Args:
        text: The text content to clean

    Returns:
        Cleaned text content
    """
    if not text:
        return ""

    # Basic text cleaning
    cleaned = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    cleaned = re.sub(r'[^\w\s.,;:!?-]', '', cleaned)  # Remove special chars
    return cleaned.strip()

