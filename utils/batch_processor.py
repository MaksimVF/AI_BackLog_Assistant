
"""
Batch Processing System for AI Agents

This module provides batch processing capabilities for agents that can tolerate
delayed processing, improving efficiency by combining multiple requests.
"""

import time
import threading
import queue
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import logging
from uuid import uuid4

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class BatchRequest:
    """Represents a single request in a batch"""
    request_id: str
    request_data: Any
    callback: Optional[Callable] = None
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

class BatchProcessor:
    """
    Batch processor for handling multiple requests efficiently.

    Args:
        batch_size: Maximum number of requests per batch
        max_wait_time: Maximum time to wait for batch to fill (seconds)
        process_function: Function to process a batch of requests
        agent_name: Name of the agent using this processor
    """

    def __init__(
        self,
        batch_size: int = 10,
        max_wait_time: float = 2.0,
        process_function: Optional[Callable] = None,
        agent_name: str = "default_agent"
    ):
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self.process_function = process_function
        self.agent_name = agent_name
        self.request_queue = queue.Queue()
        self.processing_thread = None
        self.running = False
        self.processed_count = 0
        self.error_count = 0
        self.lock = threading.Lock()

        # Start the processing thread
        self.start()

    def start(self):
        """Start the batch processing thread"""
        if not self.running:
            self.running = True
            self.processing_thread = threading.Thread(
                target=self._process_batches,
                name=f"BatchProcessor-{self.agent_name}"
            )
            self.processing_thread.daemon = True
            self.processing_thread.start()
            logger.info(f"Batch processor started for {self.agent_name}")

    def stop(self):
        """Stop the batch processor"""
        self.running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
            logger.info(f"Batch processor stopped for {self.agent_name}")

    def submit_request(
        self,
        request_data: Any,
        callback: Optional[Callable] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Submit a request to be processed in batch.

        Args:
            request_data: The data to be processed
            callback: Optional callback function to handle results
            metadata: Optional metadata about the request

        Returns:
            request_id: Unique identifier for the request
        """
        request_id = str(uuid4())
        batch_request = BatchRequest(
            request_id=request_id,
            request_data=request_data,
            callback=callback,
            metadata=metadata or {}
        )

        self.request_queue.put(batch_request)
        logger.debug(f"Request {request_id} submitted to batch processor {self.agent_name}")

        return request_id

    def _process_batches(self):
        """Main processing loop for batch processing"""
        while self.running:
            try:
                # Wait for first request or timeout
                first_request = self.request_queue.get(timeout=self.max_wait_time)

                # If we got one request, try to collect more up to batch_size or timeout
                batch = [first_request]
                start_time = time.time()

                while (
                    len(batch) < self.batch_size and
                    (time.time() - start_time) < self.max_wait_time and
                    not self.request_queue.empty()
                ):
                    try:
                        # Get additional requests with very short timeout
                        additional_request = self.request_queue.get(timeout=0.1)
                        batch.append(additional_request)
                    except queue.Empty:
                        break

                # Process the batch
                if batch:
                    self._process_batch(batch)

            except queue.Empty:
                # No requests in queue, continue waiting
                continue
            except Exception as e:
                logger.error(f"Error in batch processor {self.agent_name}: {str(e)}")
                self.error_count += 1

    def _process_batch(self, batch: List[BatchRequest]):
        """Process a batch of requests"""
        try:
            if self.process_function:
                # Extract request data for processing
                request_data_list = [req.request_data for req in batch]
                request_ids = [req.request_id for req in batch]
                callbacks = [req.callback for req in batch]

                # Process the batch
                results = self.process_function(request_data_list)

                # Handle results
                if results and callbacks:
                    for i, result in enumerate(results):
                        if callbacks[i]:
                            try:
                                callbacks[i](result)
                            except Exception as e:
                                logger.error(f"Error in callback for request {request_ids[i]}: {str(e)}")

                with self.lock:
                    self.processed_count += len(batch)

                logger.info(f"Processed batch of {len(batch)} requests for {self.agent_name}")

            else:
                logger.warning(f"No process function defined for {self.agent_name}")

        except Exception as e:
            logger.error(f"Error processing batch for {self.agent_name}: {str(e)}")
            with self.lock:
                self.error_count += len(batch)

    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            "agent_name": self.agent_name,
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "queue_size": self.request_queue.qsize(),
            "batch_size": self.batch_size,
            "max_wait_time": self.max_wait_time
        }

class AgentBatchProcessor:
    """
    Specialized batch processor for AI agents that handles common agent operations.

    This processor can handle:
    - Document classification
    - Text summarization
    - Reflection and analysis
    - Knowledge graph updates
    """

    def __init__(
        self,
        agent_type: str,
        batch_size: int = 5,
        max_wait_time: float = 1.5
    ):
        self.agent_type = agent_type
        self.processor = BatchProcessor(
            batch_size=batch_size,
            max_wait_time=max_wait_time,
            agent_name=f"agent-{agent_type}"
        )

        # Set the appropriate process function based on agent type
        if agent_type == "classifier":
            self.processor.process_function = self._process_classification_batch
        elif agent_type == "summarizer":
            self.processor.process_function = self._process_summarization_batch
        elif agent_type == "reflector":
            self.processor.process_function = self._process_reflection_batch
        elif agent_type == "knowledge_graph":
            self.processor.process_function = self._process_kg_batch
        else:
            self.processor.process_function = self._process_generic_batch

    def submit(self, data: Any, callback: Optional[Callable] = None) -> str:
        """Submit data for batch processing"""
        return self.processor.submit_request(data, callback)

    def _process_classification_batch(self, batch_data: List[Any]) -> List[Any]:
        """Process a batch of classification requests"""
        # This would call the actual classification agent
        # For now, return mock results
        return [{"class": "document", "confidence": 0.95} for _ in batch_data]

    def _process_summarization_batch(self, batch_data: List[Any]) -> List[Any]:
        """Process a batch of summarization requests"""
        # This would call the actual summarization agent
        # For now, return mock results
        return [{"summary": "Summary of document", "length": 120} for _ in batch_data]

    def _process_reflection_batch(self, batch_data: List[Any]) -> List[Any]:
        """Process a batch of reflection requests"""
        # This would call the actual reflection agent
        # For now, return mock results
        return [{"reflection": "Reflection result", "insights": []} for _ in batch_data]

    def _process_kg_batch(self, batch_data: List[Any]) -> List[Any]:
        """Process a batch of knowledge graph updates"""
        # This would call the actual KG agent
        # For now, return mock results
        return [{"status": "updated", "entities": 5} for _ in batch_data]

    def _process_generic_batch(self, batch_data: List[Any]) -> List[Any]:
        """Process a generic batch"""
        # For agents without specific batch processing
        return [{"status": "processed", "result": "generic"} for _ in batch_data]

    def get_stats(self) -> Dict[str, Any]:
        """Get processor statistics"""
        stats = self.processor.get_stats()
        stats["agent_type"] = self.agent_type
        return stats

# Global batch processors registry
class BatchProcessorRegistry:
    """Registry for managing multiple batch processors"""

    def __init__(self):
        self.processors = {}
        self.lock = threading.Lock()

    def get_processor(
        self,
        agent_type: str,
        batch_size: int = 5,
        max_wait_time: float = 1.5
    ) -> AgentBatchProcessor:
        """Get or create a batch processor for an agent type"""
        with self.lock:
            if agent_type not in self.processors:
                self.processors[agent_type] = AgentBatchProcessor(
                    agent_type=agent_type,
                    batch_size=batch_size,
                    max_wait_time=max_wait_time
                )
            return self.processors[agent_type]

    def get_all_stats(self) -> Dict[str, Any]:
        """Get statistics for all processors"""
        stats = {}
        for agent_type, processor in self.processors.items():
            stats[agent_type] = processor.get_stats()
        return stats

    def shutdown(self):
        """Shutdown all processors"""
        for processor in self.processors.values():
            processor.processor.stop()

# Global registry instance
batch_registry = BatchProcessorRegistry()

def get_batch_processor(agent_type: str, **kwargs) -> AgentBatchProcessor:
    """Get a batch processor for a specific agent type"""
    return batch_registry.get_processor(agent_type, **kwargs)

def shutdown_all_processors():
    """Shutdown all batch processors"""
    batch_registry.shutdown()
