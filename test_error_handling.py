


from logger import setup_logger, get_logger
from custom_exceptions import DataProcessingError, ConfigurationError

# Initialize loggers
setup_logger()
logger = get_logger()

# Try to set up ClickHouse logger, but handle connection errors
try:
    from clickhouse_logger import setup_clickhouse_logger
    ch_logger = setup_clickhouse_logger()
except Exception as e:
    logger.warning(f"ClickHouse logger not available: {e}")
    ch_logger = None

def test_error_handling():
    """Test the error handling and logging implementation."""
    try:
        logger.info("Starting error handling test")
        ch_logger.log_to_clickhouse('INFO', 'Starting error handling test')

        # Test data processing error
        try:
            raise DataProcessingError("Test data processing error")
        except DataProcessingError as e:
            logger.error(f"Caught DataProcessingError: {e}")
            ch_logger.log_to_clickhouse('ERROR', f"Caught DataProcessingError: {e}", 'DATA_ERROR')

        # Test configuration error
        try:
            raise ConfigurationError("Test configuration error")
        except ConfigurationError as e:
            logger.error(f"Caught ConfigurationError: {e}")
            ch_logger.log_to_clickhouse('ERROR', f"Caught ConfigurationError: {e}", 'CONFIG_ERROR')

        # Test unexpected error
        try:
            raise ValueError("Test unexpected error")
        except Exception as e:
            logger.error(f"Caught unexpected error: {e}")
            ch_logger.log_to_clickhouse('ERROR', f"Caught unexpected error: {e}", 'UNEXPECTED_ERROR')

        logger.info("Error handling test completed successfully")
        ch_logger.log_to_clickhouse('INFO', 'Error handling test completed successfully')

    except Exception as e:
        logger.error(f"Error in test_error_handling: {e}")
        ch_logger.log_to_clickhouse('ERROR', f"Error in test_error_handling: {e}", 'TEST_ERROR')

if __name__ == "__main__":
    test_error_handling()

