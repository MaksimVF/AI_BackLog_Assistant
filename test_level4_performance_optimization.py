







"""
Test Performance Optimization

Comprehensive test suite for the performance optimization capabilities.
"""

import logging
import time
from src.v2.agents.level4.visualization.performance_optimizer import PerformanceOptimizer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_performance_optimization():
    """Test the performance optimization capabilities"""
    print("Testing Performance Optimization...")

    # Generate large dataset
    large_data = []
    for i in range(1000):
        large_data.append({
            "id": i,
            "title": f"Task {i}",
            "priority": "high" if i % 3 == 0 else "medium" if i % 3 == 1 else "low",
            "category": "security" if i % 4 == 0 else "ui" if i % 4 == 1 else "docs" if i % 4 == 2 else "api",
            "value": i % 10 + 1
        })

    # Test performance optimizer
    print("\nTesting PerformanceOptimizer...")
    optimizer = PerformanceOptimizer()

    # Test streaming processing
    print("\nTesting streaming processing...")
    def process_func(data):
        # Simulate processing
        time.sleep(0.01)  # Simulate processing time
        return [item for item in data if item.get("priority") == "high"]

    streaming_result = optimizer.optimize_processing(large_data, process_func)
    print(f"✅ Streaming processing result: {len(streaming_result)} items")

    # Test parallel processing
    print("\nTesting parallel processing...")
    parallel_result = optimizer.parallel_process(large_data, process_func, 4)
    print(f"✅ Parallel processing result: {len(parallel_result)} items")

    # Test performance measurement
    print("\nTesting performance measurement...")
    def test_func():
        time.sleep(0.1)  # Simulate processing time
        return "test result"

    performance_metrics = optimizer.measure_performance(test_func)
    print(f"✅ Performance metrics: {performance_metrics}")

    # Test data structure optimization
    print("\nTesting data structure optimization...")
    optimized_data = optimizer.optimize_data_structure(large_data[:10])
    print(f"✅ Optimized data structure: {len(optimized_data)} items")

    # Test optimization recommendations
    print("\nTesting optimization recommendations...")
    recommendations = optimizer.get_optimization_recommendations(large_data)
    print(f"✅ Optimization recommendations: {recommendations}")

    print("\n🎉 All performance optimization tests completed successfully!")

if __name__ == "__main__":
    test_performance_optimization()








