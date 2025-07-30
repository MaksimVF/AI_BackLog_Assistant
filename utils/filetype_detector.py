



"""
File type detection utilities.
"""

import os
import mimetypes
import logging
from typing import Optional

def detect_filetype(file_path: str) -> str:
    """
    Detect the file type based on extension and MIME type.

    Args:
        file_path: Path to the file

    Returns:
        Detected file type
    """
    try:
        # Get file extension
        extension = os.path.splitext(file_path)[-1].lower()

        # Get MIME type
        mime_type, _ = mimetypes.guess_type(file_path)

        # Map to common types
        if extension in ['.pdf']:
            return 'pdf'
        elif extension in ['.docx', '.doc']:
            return 'word'
        elif extension in ['.txt', '.csv']:
            return 'text'
        elif extension in ['.xlsx', '.xls']:
            return 'excel'
        elif mime_type and 'image' in mime_type:
            return 'image'
        else:
            return 'unknown'

    except Exception as e:
        logging.error(f"Error detecting file type for {file_path}: {e}")
        return 'unknown'


