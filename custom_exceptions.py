

class CustomError(Exception):
    """Custom exception for handling application-specific errors."""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code
        self.message = message

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

