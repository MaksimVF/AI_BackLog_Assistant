

"""
Common utility functions for AI Backlog Assistant
"""

import logging
import os
from typing import Any, Dict

def setup_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """Set up logging configuration"""
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=logging_format,
        handlers=[
            logging.StreamHandler(),
            *([logging.FileHandler(log_file)] if log_file else [])
        ]
    )

def sanitize_input(data: Any) -> Dict:
    """Sanitize input data to prevent security issues"""
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    elif isinstance(data, str):
        # Basic sanitization - remove potentially harmful characters
        return data.replace('\n', ' ').replace('\r', ' ').strip()
    else:
        return data

def ensure_directory(path: str) -> None:
    """Ensure a directory exists"""
    os.makedirs(path, exist_ok=True)

