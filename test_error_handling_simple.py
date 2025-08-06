


from logger import setup_logger, get_logger
from custom_exceptions import DataProcessingError, ConfigurationError

# Initialize loggers
setup_logger()
logger = get_logger()

def test_error_handling():
    """Test the error handling and logging implementation."""
    try:
        logger.info("Starting error handling test")

        # Test data processing error
        try:
            raise DataProcessingError("Test data processing error")
        except DataProcessingError as e:
            logger.error(f"Caught DataProcessingError: {e}")

        # Test configuration error
        try:
            raise ConfigurationError("Test configuration error")
        except ConfigurationError as e:
            logger.error(f"Caught ConfigurationError: {e}")

        # Test unexpected error
        try:
            raise ValueError("Test unexpected error")
        except Exception as e:
            logger.error(f"Caught unexpected error: {e}")

        logger.info("Error handling test completed successfully")

    except Exception as e:
        logger.error(f"Error in test_error_handling: {e}")

if __name__ == "__main__":
    test_error_handling()


