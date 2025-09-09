
"""
Base Pipeline Class

Provides common functionality for all pipelines including:
- Input validation
- Output validation
- Error handling
- Logging
- Performance tracking
"""

from typing import Dict, Any, Optional
import time
import logging
from pydantic import BaseModel, ValidationError

class PipelineError(Exception):
    """Base exception for pipeline errors"""
    pass

class ValidationError(PipelineError):
    """Raised when input/output validation fails"""
    pass

class ProcessingError(PipelineError):
    """Raised when processing fails"""
    pass

class PipelineConfig(BaseModel):
    """Configuration for pipeline behavior"""
    enable_logging: bool = True
    enable_performance_tracking: bool = True
    timeout_seconds: Optional[int] = None
    max_retries: int = 1

class BasePipeline:
    """
    Base class for all pipelines with common functionality.
    """

    def __init__(self, config: Optional[PipelineConfig] = None):
        """
        Initialize the pipeline with configuration.

        Args:
            config: Pipeline configuration
        """
        self.config = config or PipelineConfig()
        self.logger = self._setup_logger() if self.config.enable_logging else None
        self.start_time = None

    def _setup_logger(self):
        """Set up pipeline logger"""
        logger = logging.getLogger(f"pipeline_{self.__class__.__name__}")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _log(self, message: str, level: str = "info"):
        """Log a message if logging is enabled"""
        if self.logger:
            if level == "info":
                self.logger.info(message)
            elif level == "warning":
                self.logger.warning(message)
            elif level == "error":
                self.logger.error(message)

    def _validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input data structure.

        Args:
            data: Input data to validate

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # To be implemented by subclasses
        return data

    def _validate_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate output data structure.

        Args:
            data: Output data to validate

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        # To be implemented by subclasses
        return data

    def _track_performance(self, start_time: float, end_time: float):
        """Track and log performance metrics"""
        if self.config.enable_performance_tracking:
            duration = end_time - start_time
            self._log(f"Pipeline processing time: {duration:.3f} seconds")

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the pipeline.

        Args:
            data: Input data

        Returns:
            Processed output data

        Raises:
            PipelineError: If processing fails
        """
        try:
            # Validate input
            validated_data = self._validate_input(data)

            # Track performance
            start_time = time.time()

            # Process data (to be implemented by subclasses)
            result = self._process(validated_data)

            # Validate output
            validated_result = self._validate_output(result)

            # Track performance
            end_time = time.time()
            self._track_performance(start_time, end_time)

            return validated_result

        except ValidationError as e:
            self._log(f"Validation error: {e}", "error")
            raise
        except Exception as e:
            self._log(f"Processing error: {e}", "error")
            raise ProcessingError(f"Pipeline processing failed: {e}")

    def _process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core processing logic to be implemented by subclasses.

        Args:
            data: Validated input data

        Returns:
            Processed data
        """
        raise NotImplementedError("Subclasses must implement _process method")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        pass
