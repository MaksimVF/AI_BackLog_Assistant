








"""
LangGraph Pipeline

Provides advanced processing pipeline with:
- Graph-based document classification
- Contextual prioritization
- Enhanced reflection analysis
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List
from src.v2.agents.langgraph.document_classifier import LangGraphDocumentClassifier
from src.v2.agents.langgraph.prioritization_agent import LangGraphPrioritizationAgent
from src.v2.agents.langgraph.reflection_agent import LangGraphReflectionAgent

logger = logging.getLogger(__name__)

class LangGraphPipeline:
    """Advanced processing pipeline using LangGraph agents"""

    def __init__(self, max_workers: int = 4):
        """
        Initialize LangGraph pipeline

        Args:
            max_workers: Maximum number of parallel workers
        """
        self.max_workers = max_workers

        # Initialize LangGraph agents
        self.classifier = LangGraphDocumentClassifier()
        self.prioritizer = LangGraphPrioritizationAgent()
        self.reflector = LangGraphReflectionAgent()

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through LangGraph pipeline

        Args:
            input_data: Data from Level 1 processing

        Returns:
            Processed data with LangGraph analysis
        """
        try:
            # Start processing
            start_time = time.time()

            # Step 1: Graph-based classification
            classified_data = self.classifier.classify(input_data)

            # Step 2: Graph-based prioritization
            prioritized_data = self.prioritizer.prioritize(classified_data)

            # Step 3: Graph-based reflection
            reflected_data = self.reflector.analyze(prioritized_data)

            # Calculate processing time
            processing_time = time.time() - start_time

            # Add monitoring data
            reflected_data["_monitoring"] = {
                "status": "success",
                "processing_time": processing_time,
                "steps_completed": 3
            }

            logger.info(f"LangGraph processing completed in {processing_time:.2f} seconds")

            return reflected_data

        except Exception as e:
            logger.error(f"LangGraph processing failed: {e}")
            # Add fallback processing
            return {
                **input_data,
                "_monitoring": {
                    "status": "error",
                    "error": str(e),
                    "processing_time": time.time() - start_time
                }
            }

    def process_batch(self, batch_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process batch of data through LangGraph pipeline

        Args:
            batch_data: List of data items from Level 1

        Returns:
            List of processed data with LangGraph analysis
        """
        try:
            # Process batch in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                results = list(executor.map(self.process, batch_data))

            logger.info(f"Processed batch of {len(batch_data)} documents")

            return results

        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            # Add fallback batch processing
            return [
                {
                    **data,
                    "_monitoring": {
                        "status": "error",
                        "error": str(e),
                        "processing_time": 0
                    }
                }
                for data in batch_data
            ]

    def process_with_monitoring(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data with detailed monitoring

        Args:
            input_data: Data from Level 1 processing

        Returns:
            Processed data with detailed monitoring
        """
        try:
            # Start processing
            start_time = time.time()

            # Process through pipeline
            result = self.process(input_data)

            # Add detailed monitoring
            result["_monitoring"]["detailed"] = {
                "classification": result.get("classification", {}),
                "prioritization": result.get("prioritization", {}),
                "reflection": result.get("reflection", {})
            }

            logger.info(f"Detailed monitoring completed for {input_data.get('document_id', 'unknown')}")

            return result

        except Exception as e:
            logger.error(f"Monitored processing failed: {e}")
            # Add fallback monitoring
            return {
                **input_data,
                "_monitoring": {
                    "status": "error",
                    "error": str(e),
                    "processing_time": time.time() - start_time
                }
            }

    def process_with_feedback(self, input_data: Dict[str, Any], feedback_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process data with feedback integration

        Args:
            input_data: Data from Level 1 processing
            feedback_data: Feedback data for improvement

        Returns:
            Processed data with feedback integration
        """
        try:
            # Process through pipeline
            result = self.process(input_data)

            # Integrate feedback if provided
            if feedback_data:
                result["feedback_integration"] = {
                    "feedback_processed": True,
                    "feedback_data": feedback_data
                }

            logger.info(f"Feedback integration completed for {input_data.get('document_id', 'unknown')}")

            return result

        except Exception as e:
            logger.error(f"Feedback processing failed: {e}")
            # Add fallback feedback processing
            return {
                **input_data,
                "_monitoring": {
                    "status": "error",
                    "error": str(e),
                    "processing_time": 0
                }
            }

    def classify_with_graph(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform graph-based classification

        Args:
            input_data: Data from Level 1 processing

        Returns:
            Classification result
        """
        try:
            # Perform classification
            result = self.classifier.classify(input_data)

            # Add monitoring
            result["_monitoring"] = {
                "status": "success",
                "processing_time": 0,
                "steps_completed": 1
            }

            logger.info(f"Graph classification completed for {input_data.get('document_id', 'unknown')}")

            return result

        except Exception as e:
            logger.error(f"Graph classification failed: {e}")
            # Add fallback classification
            return {
                **input_data,
                "_monitoring": {
                    "status": "error",
                    "error": str(e),
                    "processing_time": 0
                }
            }

    def prioritize_with_graph(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform graph-based prioritization

        Args:
            input_data: Data from Level 1 and classification

        Returns:
            Prioritization result
        """
        try:
            # Perform prioritization
            result = self.prioritizer.prioritize(input_data)

            # Add monitoring
            result["_monitoring"] = {
                "status": "success",
                "processing_time": 0,
                "steps_completed": 1
            }

            logger.info(f"Graph prioritization completed for {input_data.get('document_id', 'unknown')}")

            return result

        except Exception as e:
            logger.error(f"Graph prioritization failed: {e}")
            # Add fallback prioritization
            return {
                **input_data,
                "_monitoring": {
                    "status": "error",
                    "error": str(e),
                    "processing_time": 0
                }
            }

    def analyze_with_graph(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform graph-based reflection analysis

        Args:
            input_data: Data from Level 1, classification, and prioritization

        Returns:
            Reflection analysis result
        """
        try:
            # Perform reflection analysis
            result = self.reflector.analyze(input_data)

            # Add monitoring
            result["_monitoring"] = {
                "status": "success",
                "processing_time": 0,
                "steps_completed": 1
            }

            logger.info(f"Graph reflection analysis completed for {input_data.get('document_id', 'unknown')}")

            return result

        except Exception as e:
            logger.error(f"Graph reflection analysis failed: {e}")
            # Add fallback reflection analysis
            return {
                **input_data,
                "_monitoring": {
                    "status": "error",
                    "error": str(e),
                    "processing_time": 0
                }
            }








