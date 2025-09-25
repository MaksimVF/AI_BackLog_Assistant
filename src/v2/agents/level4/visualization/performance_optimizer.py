







"""
Performance Optimizer

Enhanced performance optimization for visualization processing.
"""

import logging
import time
from typing import List, Dict, Any, Callable, Optional
from functools import lru_cache
from crewai import Agent

logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """
    Optimizes performance for visualization processing with advanced techniques.
    """

    def __init__(self):
        """
        Initialize performance optimizer with CrewAI agent.
        """
        # Initialize CrewAI agent for performance optimization
        self.agent = Agent(
            name="PerformanceOptimizer",
            role="Performance optimization agent for visualization processing",
            goal="""
                Optimize performance for visualization processing.
                Implement streaming, caching, and parallel processing.
            """,
            backstory="""
                You are a performance optimization agent that uses
                advanced techniques to improve visualization processing.
            """,
            tools=[],
            verbose=True
        )

    def optimize_processing(self, data: List[Dict[str, Any]], process_func: Callable[[List[Dict[str, Any]]], Any]) -> Any:
        """
        Optimize processing with streaming and caching.

        Args:
            data: Data to process
            process_func: Processing function

        Returns:
            Processed results with performance optimization
        """
        try:
            # Use streaming for large datasets
            if len(data) > 1000:
                return self._streaming_process(data, process_func)
            else:
                return self._cached_process(data, process_func)

        except Exception as e:
            logger.error(f"Performance optimization failed: {e}")
            raise

    def _streaming_process(self, data: List[Dict[str, Any]], process_func: Callable[[List[Dict[str, Any]]], Any]) -> Any:
        """
        Process data in streaming mode for large datasets.

        Args:
            data: Data to process
            process_func: Processing function

        Returns:
            Processed results with streaming optimization
        """
        try:
            # Process data in chunks
            chunk_size = 500
            results = []

            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                result = process_func(chunk)
                results.append(result)

                # Log progress
                logger.info(f"Processed chunk {i//chunk_size + 1} with {len(chunk)} items")

            # Combine results
            combined_result = self._combine_results(results)
            return combined_result

        except Exception as e:
            logger.error(f"Streaming processing failed: {e}")
            raise

    def _cached_process(self, data: List[Dict[str, Any]], process_func: Callable[[List[Dict[str, Any]]], Any]) -> Any:
        """
        Process data with caching for smaller datasets.

        Args:
            data: Data to process
            process_func: Processing function

        Returns:
            Processed results with caching optimization
        """
        try:
            # Use caching for repeated operations
            @lru_cache(maxsize=128)
            def cached_process(data_tuple):
                # Convert tuple back to list of dicts
                data_list = [dict(item) for item in data_tuple]
                return process_func(data_list)

            # Convert data to hashable format
            data_tuple = tuple(tuple(item.items()) for item in data)
            result = cached_process(data_tuple)

            logger.info("Processed data with caching optimization")
            return result

        except Exception as e:
            logger.error(f"Cached processing failed: {e}")
            raise

    def _combine_results(self, results: List[Any]) -> Any:
        """
        Combine results from streaming processing.

        Args:
            results: List of results

        Returns:
            Combined result
        """
        # Simple combination for demonstration
        if isinstance(results[0], list):
            combined = []
            for result in results:
                combined.extend(result)
            return combined
        else:
            # For other types, return the last result
            return results[-1] if results else None

    def parallel_process(self, data: List[Dict[str, Any]], process_func: Callable[[List[Dict[str, Any]]], Any], num_workers: int = 4) -> Any:
        """
        Process data in parallel for performance optimization.

        Args:
            data: Data to process
            process_func: Processing function
            num_workers: Number of parallel workers

        Returns:
            Processed results with parallel optimization
        """
        try:
            from concurrent.futures import ThreadPoolExecutor

            # Split data into chunks
            chunk_size = len(data) // num_workers + 1
            chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

            # Process chunks in parallel
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                results = list(executor.map(process_func, chunks))

            # Combine results
            combined_result = self._combine_results(results)

            logger.info(f"Processed data in parallel with {num_workers} workers")
            return combined_result

        except Exception as e:
            logger.error(f"Parallel processing failed: {e}")
            raise

    def measure_performance(self, process_func: Callable[[], Any]) -> Dict[str, Any]:
        """
        Measure performance of a processing function.

        Args:
            process_func: Function to measure

        Returns:
            Performance metrics
        """
        try:
            start_time = time.time()
            result = process_func()
            end_time = time.time()

            return {
                "execution_time": end_time - start_time,
                "result": result,
                "performance_score": self._calculate_performance_score(end_time - start_time)
            }

        except Exception as e:
            logger.error(f"Performance measurement failed: {e}")
            raise

    def _calculate_performance_score(self, execution_time: float) -> float:
        """
        Calculate performance score based on execution time.

        Args:
            execution_time: Execution time in seconds

        Returns:
            Performance score (0-1)
        """
        # Score calculation (simplified)
        if execution_time < 0.1:
            return 0.95
        elif execution_time < 0.5:
            return 0.85
        elif execution_time < 1.0:
            return 0.75
        else:
            return 0.65

    def optimize_data_structure(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Optimize data structure for better performance.

        Args:
            data: Data to optimize

        Returns:
            Optimized data structure
        """
        try:
            # Convert to more efficient data structure
            optimized_data = []

            # Analyze data structure
            for item in data:
                optimized_item = {
                    "id": item.get("id", str(hash(str(item)))),
                    "priority": item.get("priority", "unknown"),
                    "value": item.get("value", 0),
                    "metadata": {
                        "title": item.get("title", ""),
                        "category": item.get("category", "")
                    }
                }
                optimized_data.append(optimized_item)

            logger.info("Optimized data structure for better performance")
            return optimized_data

        except Exception as e:
            logger.error(f"Data structure optimization failed: {e}")
            raise

    def get_optimization_recommendations(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get optimization recommendations for data processing.

        Args:
            data: Data to analyze

        Returns:
            Optimization recommendations
        """
        # Analyze data size and structure
        data_size = len(data)
        avg_item_size = sum(len(str(item)) for item in data) / data_size if data_size > 0 else 0

        recommendations = {
            "data_size": data_size,
            "avg_item_size": avg_item_size,
            "recommendations": []
        }

        # Generate recommendations
        if data_size > 1000:
            recommendations["recommendations"].append("Use streaming processing for large datasets")
        if avg_item_size > 1000:
            recommendations["recommendations"].append("Optimize data structure for large items")
        if data_size > 100:
            recommendations["recommendations"].append("Consider parallel processing")

        return recommendations





