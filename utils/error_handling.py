
"""
Error Handling Framework for AI Backlog Assistant

Provides consistent error handling, logging, and reporting across the application.
"""

import logging
import traceback
from typing import Optional, Dict, Any, List
from enum import Enum
from custom_exceptions import SecurityError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("AIBacklogAssistant")

class ErrorSeverity(Enum):
    """Error severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AIBacklogError(Exception):
    """Base exception class for AI Backlog Assistant errors"""

    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        error_code: Optional[str] = None,
        original_exception: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.severity = severity
        self.error_code = error_code or f"AIBA_{severity.value.upper()}"
        self.original_exception = original_exception
        self.context = context or {}
        self.timestamp = logging.Formatter('%(asctime)s').format(logging.makeLogRecord({}))

        # Log the error
        self._log_error()

    def _log_error(self):
        """Log the error with appropriate severity"""
        log_method = getattr(logger, self.severity.value.upper(), logger.error)

        log_data = {
            "error_code": self.error_code,
            "message": str(self),
            "severity": self.severity.value,
            "context": self.context,
            "timestamp": self.timestamp
        }

        if self.original_exception:
            log_data["original_error"] = str(self.original_exception)
            log_data["traceback"] = traceback.format_exc()

        log_method(f"Error {self.error_code}: {self.message}", extra=log_data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for reporting"""
        return {
            "error_code": self.error_code,
            "message": str(self),
            "severity": self.severity.value,
            "context": self.context,
            "timestamp": self.timestamp,
            "original_error": str(self.original_exception) if self.original_exception else None
        }

class ConfigurationError(AIBacklogError):
    """Configuration related errors"""
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(
            message,
            ErrorSeverity.ERROR,
            "AIBA_CONFIG_ERROR",
            context=context
        )

class DependencyError(AIBacklogError):
    """Dependency or external service errors"""
    def __init__(self, message: str, service: str, context: Optional[Dict] = None):
        super().__init__(
            message,
            ErrorSeverity.ERROR,
            f"AIBA_{service.upper()}_ERROR",
            context=context
        )

class ProcessingError(AIBacklogError):
    """Data processing errors"""
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(
            message,
            ErrorSeverity.WARNING,
            "AIBA_PROCESSING_ERROR",
            context=context
        )

class ValidationError(AIBacklogError):
    """Input validation errors"""
    def __init__(self, message: str, field: Optional[str] = None, context: Optional[Dict] = None):
        super().__init__(
            message,
            ErrorSeverity.WARNING,
            "AIBA_VALIDATION_ERROR",
            context={"field": field, **(context or {})}
        )

def handle_exception(
    exception: Exception,
    severity: ErrorSeverity = ErrorSeverity.ERROR,
    error_code: Optional[str] = None,
    context: Optional[Dict] = None
) -> AIBacklogError:
    """
    Handle exceptions and convert them to AIBacklogError

    Args:
        exception: The original exception
        severity: Error severity level
        error_code: Custom error code
        context: Additional context information

    Returns:
        AIBacklogError instance
    """
    message = f"Unhandled exception: {str(exception)}"
    return AIBacklogError(
        message,
        severity=severity,
        error_code=error_code,
        original_exception=exception,
        context=context
    )

def log_error(
    message: str,
    severity: ErrorSeverity = ErrorSeverity.ERROR,
    error_code: Optional[str] = None,
    context: Optional[Dict] = None
):
    """
    Log an error without raising an exception

    Args:
        message: Error message
        severity: Error severity level
        error_code: Custom error code
        context: Additional context information
    """
    try:
        raise AIBacklogError(
            message,
            severity=severity,
            error_code=error_code,
            context=context
        )
    except AIBacklogError as e:
        # Only log, don't re-raise
        pass

def safe_execute(func, *args, **kwargs):
    """
    Safely execute a function with error handling

    Args:
        func: Function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Tuple of (result, error) where error is None if successful
    """
    try:
        result = func(*args, **kwargs)
        return result, None
    except Exception as e:
        error = handle_exception(e)
        return None, error

