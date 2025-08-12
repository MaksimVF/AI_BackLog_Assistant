

"""
Batch Processing Decorator for AI Agents

This module provides decorators to easily add batch processing capabilities
to agent methods.
"""

import functools
import time
from typing import Callable, Any, Optional, Dict
from .batch_processor import get_batch_processor, AgentBatchProcessor

def batch_processing(
    agent_type: str,
    batch_size: int = 5,
    max_wait_time: float = 1.5,
    result_timeout: float = 10.0
):
    """
    Decorator to add batch processing to agent methods.

    Args:
        agent_type: Type of agent (e.g., 'classifier', 'summarizer')
        batch_size: Maximum number of requests per batch
        max_wait_time: Maximum time to wait for batch to fill (seconds)
        result_timeout: Maximum time to wait for results (seconds)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get the batch processor for this agent type
            processor = get_batch_processor(
                agent_type=agent_type,
                batch_size=batch_size,
                max_wait_time=max_wait_time
            )

            # Prepare the data to be processed
            # By default, we pass all args and kwargs as the data
            # This can be customized as needed
            request_data = {
                "args": args,
                "kwargs": kwargs,
                "original_function": func.__name__
            }

            # Create a result container to store the response
            result_container = {}

            def callback(result):
                """Callback to store the result"""
                result_container["result"] = result
                result_container["timestamp"] = time.time()

            # Submit the request for batch processing
            request_id = processor.submit(request_data, callback)

            # Wait for the result (with timeout)
            start_time = time.time()
            while True:
                if "result" in result_container:
                    return result_container["result"]

                if (time.time() - start_time) > result_timeout:
                    raise TimeoutError(
                        f"Batch processing timed out after {result_timeout} seconds "
                        f"for request {request_id}"
                    )

                time.sleep(0.1)  # Small sleep to avoid busy waiting

        return wrapper

    return decorator

# Example usage:
# @batch_processing(agent_type="classifier", batch_size=3, max_wait_time=1.0)
# def classify_document(self, document_text):
#     # Original implementation
#     pass

