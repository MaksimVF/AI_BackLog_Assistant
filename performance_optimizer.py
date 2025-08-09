


"""
Performance optimization module for AI_BackLog_Assistant
"""

import os
import sys
import time
import logging
import asyncio
import functools
from typing import Dict, Any, Optional, Callable, Coroutine, TypeVar

# Add project root to path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.system_admin.logging_manager import initialize_logging
from agents.system_admin.monitoring_agent import MonitoringAgent
from redis_queue.queue_dispatcher import redis_conn

# Initialize logging
logging_manager = initialize_logging(
    service_name="PerformanceOptimizer",
    environment=os.getenv('ENV', 'dev')
)
logger = logging_manager.get_logger()

# Initialize monitoring agent
monitoring_agent = MonitoringAgent()

T = TypeVar('T')

class PerformanceOptimizer:
    """
    Performance optimization module with caching, async processing, and database optimization
    """

    def __init__(self):
        self.cache_enabled = True
        self.async_enabled = True
        self.db_optimization_enabled = True

        # Initialize Redis cache
        self.cache = redis_conn
        logger.info("Performance optimizer initialized")

    def enable_caching(self, enable: bool = True):
        """Enable or disable caching"""
        self.cache_enabled = enable
        logger.info(f"Caching {'enabled' if enable else 'disabled'}")

    def enable_async(self, enable: bool = True):
        """Enable or disable async processing"""
        self.async_enabled = enable
        logger.info(f"Async processing {'enabled' if enable else 'disabled'}")

    def enable_db_optimization(self, enable: bool = True):
        """Enable or disable database optimization"""
        self.db_optimization_enabled = enable
        logger.info(f"Database optimization {'enabled' if enable else 'disabled'}")

    def cache_result(self, key: str, value: Any, expires: int = 3600) -> bool:
        """
        Cache a result in Redis

        Args:
            key: Cache key
            value: Value to cache
            expires: Expiration time in seconds

        Returns:
            True if caching succeeded, False otherwise
        """
        if not self.cache_enabled:
            return False

        try:
            # Serialize the value (simple approach, could be improved)
            if isinstance(value, (int, float, str, bool)):
                cached_value = str(value)
            else:
                import json
                cached_value = json.dumps(value)

            self.cache.setex(key, expires, cached_value)
            logger.debug(f"Cached result for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to cache result: {e}")
            return False

    def get_cached_result(self, key: str, default: Any = None) -> Any:
        """
        Get a cached result from Redis

        Args:
            key: Cache key
            default: Default value to return if cache miss

        Returns:
            Cached value or default
        """
        if not self.cache_enabled:
            return default

        try:
            cached_value = self.cache.get(key)
            if cached_value is None:
                return default

            # Try to deserialize
            try:
                import json
                return json.loads(cached_value)
            except (json.JSONDecodeError, TypeError):
                return cached_value

        except Exception as e:
            logger.error(f"Failed to get cached result: {e}")
            return default

    def cache_decorator(self, expires: int = 3600):
        """
        Decorator for caching function results

        Args:
            expires: Cache expiration time in seconds

        Returns:
            Decorator function
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.cache_enabled:
                    return func(*args, **kwargs)

                # Generate cache key from function name and arguments
                key_parts = [func.__name__]
                key_parts.extend([str(arg) for arg in args])
                key_parts.extend([f"{k}={v}" for k, v in kwargs.items()])
                cache_key = f"func_cache:{':'.join(key_parts)}"

                # Try to get from cache
                cached_result = self.get_cached_result(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for: {cache_key}")
                    return cached_result

                # Call the function and cache the result
                result = func(*args, **kwargs)
                self.cache_result(cache_key, result, expires)
                return result

            return wrapper

        return decorator

    async def async_task(self, func: Callable[..., Coroutine], *args, **kwargs) -> Any:
        """
        Run a function as an async task

        Args:
            func: Function to run asynchronously
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Result of the function
        """
        if not self.async_enabled:
            return await func(*args, **kwargs)

        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Async task failed: {e}")
            raise

    def optimize_database_query(self, query: str, params: Optional[dict] = None) -> str:
        """
        Optimize a database query

        Args:
            query: SQL query to optimize
            params: Query parameters

        Returns:
            Optimized query
        """
        if not self.db_optimization_enabled:
            return query

        # Simple query optimization examples
        optimized_query = query

        # Add query hints for large result sets
        if "SELECT" in query.upper() and "LIMIT" not in query.upper():
            optimized_query = query + " LIMIT 1000"

        # Ensure proper indexing hints
        if "JOIN" in query.upper() and "INDEX" not in query.upper():
            # This is a simple example, real optimization would be more sophisticated
            optimized_query = query.replace("JOIN", "JOIN /*+ INDEX(table_index) */")

        logger.debug(f"Optimized query: {optimized_query}")
        return optimized_query

    def get_system_performance(self) -> Dict[str, Any]:
        """
        Get current system performance metrics

        Returns:
            Dictionary with performance metrics
        """
        try:
            status = monitoring_agent.get_system_status()
            return {
                'cpu_usage': status.get('cpu', {}).get('percent', 0),
                'memory_usage': status.get('memory', {}).get('virtual', {}).get('percent', 0),
                'disk_usage': status.get('disk', {}).get('usage', {}).get('percent', 0),
                'process_count': status.get('processes', {}).get('count', 0),
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Failed to get system performance: {e}")
            return {}

    def analyze_performance_bottlenecks(self) -> Dict[str, Any]:
        """
        Analyze system performance and identify bottlenecks

        Returns:
            Dictionary with bottleneck analysis
        """
        try:
            performance = self.get_system_performance()
            bottlenecks = []

            if performance['cpu_usage'] > 80:
                bottlenecks.append({
                    'type': 'cpu',
                    'level': 'high' if performance['cpu_usage'] > 90 else 'medium',
                    'value': performance['cpu_usage']
                })

            if performance['memory_usage'] > 80:
                bottlenecks.append({
                    'type': 'memory',
                    'level': 'high' if performance['memory_usage'] > 90 else 'medium',
                    'value': performance['memory_usage']
                })

            if performance['disk_usage'] > 80:
                bottlenecks.append({
                    'type': 'disk',
                    'level': 'high' if performance['disk_usage'] > 90 else 'medium',
                    'value': performance['disk_usage']
                })

            if performance['process_count'] > 500:
                bottlenecks.append({
                    'type': 'process_count',
                    'level': 'high' if performance['process_count'] > 1000 else 'medium',
                    'value': performance['process_count']
                })

            return {
                'bottlenecks': bottlenecks,
                'performance': performance,
                'timestamp': time.time()
            }

        except Exception as e:
            logger.error(f"Failed to analyze performance: {e}")
            return {'bottlenecks': [], 'error': str(e)}

    def get_optimization_recommendations(self) -> Dict[str, Any]:
        """
        Get performance optimization recommendations

        Returns:
            Dictionary with recommendations
        """
        try:
            analysis = self.analyze_performance_bottlenecks()
            recommendations = []

            for bottleneck in analysis['bottlenecks']:
                if bottleneck['type'] == 'cpu':
                    if bottleneck['level'] == 'high':
                        recommendations.append({
                            'type': 'critical',
                            'message': 'CPU usage is critically high',
                            'action': 'Add more CPU resources or optimize processes'
                        })
                    else:
                        recommendations.append({
                            'type': 'warning',
                            'message': 'CPU usage is elevated',
                            'action': 'Monitor CPU usage and optimize if needed'
                        })

                elif bottleneck['type'] == 'memory':
                    if bottleneck['level'] == 'high':
                        recommendations.append({
                            'type': 'critical',
                            'message': 'Memory usage is critically high',
                            'action': 'Add more RAM or optimize memory usage'
                        })
                    else:
                        recommendations.append({
                            'type': 'warning',
                            'message': 'Memory usage is elevated',
                            'action': 'Monitor memory usage and optimize if needed'
                        })

                elif bottleneck['type'] == 'disk':
                    if bottleneck['level'] == 'high':
                        recommendations.append({
                            'type': 'critical',
                            'message': 'Disk usage is critically high',
                            'action': 'Free up disk space immediately'
                        })
                    else:
                        recommendations.append({
                            'type': 'warning',
                            'message': 'Disk usage is elevated',
                            'action': 'Plan to free up disk space'
                        })

                elif bottleneck['type'] == 'process_count':
                    if bottleneck['level'] == 'high':
                        recommendations.append({
                            'type': 'critical',
                            'message': 'Process count is critically high',
                            'action': 'Investigate process leaks'
                        })
                    else:
                        recommendations.append({
                            'type': 'warning',
                            'message': 'Process count is elevated',
                            'action': 'Monitor process count'
                        })

            return {
                'recommendations': recommendations,
                'analysis': analysis,
                'timestamp': time.time()
            }

        except Exception as e:
            logger.error(f"Failed to get recommendations: {e}")
            return {'recommendations': [], 'error': str(e)}

# Create a global performance optimizer instance
performance_optimizer = PerformanceOptimizer()

if __name__ == "__main__":
    # Test the performance optimizer
    print("Testing performance optimizer...")

    # Test caching
    @performance_optimizer.cache_decorator(expires=60)
    def test_function(x, y):
        print(f"Computing {x} + {y} (this should only appear once)")
        return x + y

    print(f"Result 1: {test_function(5, 3)}")
    print(f"Result 2: {test_function(5, 3)}")  # Should use cache
    print(f"Result 3: {test_function(10, 3)}")  # Should compute

    # Test performance analysis
    analysis = performance_optimizer.analyze_performance_bottlenecks()
    print(f"Bottlenecks found: {len(analysis['bottlenecks'])}")

    # Test recommendations
    recommendations = performance_optimizer.get_optimization_recommendations()
    print(f"Recommendations: {len(recommendations['recommendations'])}")

    print("Performance optimizer test completed")

