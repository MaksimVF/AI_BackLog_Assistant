
from loguru import logger

def setup_logger():
    """Set up the logger with file rotation and formatting."""
    logger.add(
        "app.log",
        rotation="500 MB",  # Rotate log files when they reach 500MB
        level="INFO",       # Set default logging level
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"  # Custom format
    )

def get_logger():
    """Get the configured logger instance."""
    return logger
