

"""
Level 2 Processing Pipeline

Enhanced with parallel processing, error handling, and monitoring.

Coordinates the flow of data through Level 2 agents for:
1. Categorization
2. Prioritization
3. Reflection

Input: Processed data from Level 1
Output: Analyzed and categorized data ready for Level 3
"""

import logging
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor
from src.v2.agents.level2.categorization.document_classifier import DocumentClassifierAgent
from src.v2.agents.level2.prioritization.prioritization_agent import PrioritizationAgent
from src.v2.agents.level2.reflection.reflection_agent import ReflectionAgent

logger = logging.getLogger(__name__)

class Level2Pipeline:
    """Coordinates Level 2 processing with enhanced features"""

    def __init__(self, max_workers: int = 4):
        """
        Initialize Level 2 pipeline with configuration

        Args:
            max_workers: Maximum number of parallel workers
        """
        self.max_workers = max_workers

        # Initialize Level 2 agents with configuration
        self.document_classifier = DocumentClassifierAgent(cache_size=2000)
        self.prioritization_agent = PrioritizationAgent()
        self.reflection_agent = ReflectionAgent()

    def process(self, level1_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through Level 2 pipeline with enhanced error handling

        Args:
            level1_data: Processed data from Level 1 pipeline

        Returns:
            Analyzed and categorized data

        Raises:
            PipelineError: If processing fails at any stage
        """
        try:
            # Validate input
            if not level1_data or "content" not in level1_data:
                logger.error("Invalid input data for Level 2 processing")
                raise ValueError("Invalid input data")

            # Step 1: Document classification
            logger.info(f"Level 2: Starting document classification for {level1_data.get('document_id', 'unknown')}")
            classified_data = self.document_classifier.classify(level1_data)

            # Step 2: Prioritization
            logger.info(f"Level 2: Starting prioritization for {level1_data.get('document_id', 'unknown')}")
            prioritized_data = self.prioritization_agent.prioritize(classified_data)

            # Step 3: Reflection
            logger.info(f"Level 2: Starting reflection analysis for {level1_data.get('document_id', 'unknown')}")
            reflected_data = self.reflection_agent.analyze(prioritized_data)

            logger.info(f"Level 2: Successfully processed {level1_data.get('document_id', 'unknown')}")
            return reflected_data

        except Exception as e:
            logger.error(f"Level 2 processing failed for {level1_data.get('document_id', 'unknown')}: {e}")
            raise

    def process_batch(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple documents in parallel

        Args:
            documents: List of documents to process

        Returns:
            List of processed documents
        """
        try:
            logger.info(f"Level 2: Starting batch processing of {len(documents)} documents")

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                results = list(executor.map(self.process, documents))

            logger.info("Level 2: Completed batch processing")
            return results

        except Exception as e:
            logger.error(f"Level 2 batch processing failed: {e}")
            raise

    def process_with_monitoring(self, level1_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data with performance monitoring

        Args:
            level1_data: Processed data from Level 1 pipeline

        Returns:
            Processed data with monitoring metrics
        """
        import time

        start_time = time.time()
        try:
            result = self.process(level1_data)
            processing_time = time.time() - start_time

            logger.info(f"Level 2: Processed {level1_data.get('document_id', 'unknown')} in {processing_time:.2f}s")

            # Add monitoring metrics
            result["_monitoring"] = {
                "processing_time": processing_time,
                "status": "success"
            }

            return result

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Level 2: Processing failed after {processing_time:.2f}s: {e}")

            # Return partial result with error info
            return {
                **level1_data,
                "_monitoring": {
                    "processing_time": processing_time,
                    "status": "error",
                    "error": str(e)
                }
            }

