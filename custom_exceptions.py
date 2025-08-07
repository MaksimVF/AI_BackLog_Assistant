

class CustomError(Exception):
    """Base custom exception for handling application-specific errors."""
    def __init__(self, message, error_code=None, original_exception=None):
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.original_exception = original_exception

    def __str__(self):
        if self.original_exception:
            return f"{self.message} (Original: {str(self.original_exception)})"
        return self.message

class DataProcessingError(CustomError):
    """Exception raised when there's an error processing data."""
    pass

class DatabaseError(CustomError):
    """Exception raised when there's a database-related error."""
    pass

class APIError(CustomError):
    """Exception raised when there's an API-related error."""
    pass

class ConfigurationError(CustomError):
    """Exception raised when there's a configuration error."""
    pass

class IntegrationError(CustomError):
    """Exception raised when there's an integration error with external services."""
    pass

class MemoryError(CustomError):
    """Exception raised when there's a memory-related error."""
    pass

class ReflectionError(CustomError):
    """Exception raised when there's a reflection-related error."""
    pass

class SecurityError(CustomError):
    """Exception raised when there's a security-related error."""
    pass

class ValidationError(CustomError):
    """Exception raised when there's a data validation error."""
    pass

class RateLimitError(CustomError):
    """Exception raised when rate limits are exceeded."""
    pass

class CircuitBreakerError(CustomError):
    """Exception raised when a circuit breaker is triggered."""
    pass

class ResourceExhaustedError(CustomError):
    """Exception raised when resources are exhausted."""
    pass

class TimeoutError(CustomError):
    """Exception raised when an operation times out."""
    pass

class AgentCommunicationError(CustomError):
    """Exception raised when there's an agent communication error."""
    pass

class PipelineError(CustomError):
    """Exception raised when there's a pipeline processing error."""
    pass

class ExternalServiceError(CustomError):
    """Exception raised when there's an external service error."""
    pass

class DataFormatError(CustomError):
    """Exception raised when there's a data format error."""
    pass

class NotImplementedError(CustomError):
    """Exception raised when functionality is not implemented."""
    pass

class PermissionDeniedError(CustomError):
    """Exception raised when permission is denied."""
    pass

class AuthenticationError(CustomError):
    """Exception raised when authentication fails."""
    pass

class AuthorizationError(CustomError):
    """Exception raised when authorization fails."""
    pass

class QuotaExceededError(CustomError):
    """Exception raised when quota is exceeded."""
    pass

class ServiceUnavailableError(CustomError):
    """Exception raised when a service is unavailable."""
    pass

class RetryableError(CustomError):
    """Exception raised for errors that can be retried."""
    def __init__(self, message, error_code=None, original_exception=None, retry_after=None):
        super().__init__(message, error_code, original_exception)
        self.retry_after = retry_after

class NonRetryableError(CustomError):
    """Exception raised for errors that should not be retried."""
    pass

