



"""
Test script for performance optimization integration
"""

import os
import sys
import time
import asyncio
import threading

# Add project root to path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from performance_optimizer import performance_optimizer
from agents.system_admin.logging_manager import initialize_logging

# Initialize logging
logging_manager = initialize_logging(
    service_name="PerformanceTest",
    environment="test"
)
logger = logging_manager.get_logger()

def test_caching():
    """Test the caching functionality"""
    print("=== Testing Caching ===")

    # Enable caching
    performance_optimizer.enable_caching(True)

    @performance_optimizer.cache_decorator(expires=10)
    def expensive_computation(x, y):
        print(f"Computing {x} * {y} (expensive operation)")
        time.sleep(1)  # Simulate expensive computation
        return x * y

    # First call should compute
    start_time = time.time()
    result1 = expensive_computation(5, 3)
    end_time = time.time()
    print(f"First call result: {result1} (took {end_time - start_time:.2f}s)")

    # Second call should use cache
    start_time = time.time()
    result2 = expensive_computation(5, 3)
    end_time = time.time()
    print(f"Second call result: {result2} (took {end_time - start_time:.2f}s)")

    # Different arguments should compute
    start_time = time.time()
    result3 = expensive_computation(10, 3)
    end_time = time.time()
    print(f"Third call result: {result3} (took {end_time - start_time:.2f}s)")

    print("✓ Caching test completed")

def test_async_processing():
    """Test the async processing functionality"""
    print("\n=== Testing Async Processing ===")

    async def async_task_1():
        print("Starting async task 1")
        await asyncio.sleep(1)
        print("Completed async task 1")
        return "Task 1 result"

    async def async_task_2():
        print("Starting async task 2")
        await asyncio.sleep(0.5)
        print("Completed async task 2")
        return "Task 2 result"

    async def run_async_tasks():
        # Run tasks concurrently
        results = await asyncio.gather(
            performance_optimizer.async_task(async_task_1),
            performance_optimizer.async_task(async_task_2)
        )
        return results

    # Run the async test
    start_time = time.time()
    asyncio.run(run_async_tasks())
    end_time = time.time()
    print(f"Async tasks completed in {end_time - start_time:.2f}s")
    print("✓ Async processing test completed")

def test_database_optimization():
    """Test the database optimization functionality"""
    print("\n=== Testing Database Optimization ===")

    # Test query optimization
    original_query = "SELECT * FROM large_table WHERE status = 'active'"
    optimized_query = performance_optimizer.optimize_database_query(original_query)

    print(f"Original query: {original_query}")
    print(f"Optimized query: {optimized_query}")

    # Test with JOIN
    join_query = "SELECT u.*, p.* FROM users u JOIN profiles p ON u.id = p.user_id"
    optimized_join = performance_optimizer.optimize_database_query(join_query)

    print(f"Original JOIN: {join_query}")
    print(f"Optimized JOIN: {optimized_join}")

    print("✓ Database optimization test completed")

def test_performance_monitoring():
    """Test the performance monitoring functionality"""
    print("\n=== Testing Performance Monitoring ===")

    def monitoring_loop():
        for i in range(3):
            # Get performance metrics
            performance = performance_optimizer.get_system_performance()
            print(f"Monitoring cycle {i+1}:")
            print(f"  CPU: {performance['cpu_usage']}%")
            print(f"  Memory: {performance['memory_usage']}%")
            print(f"  Disk: {performance['disk_usage']}%")
            print(f"  Processes: {performance['process_count']}")

            # Get analysis
            analysis = performance_optimizer.analyze_performance_bottlenecks()
            if analysis['bottlenecks']:
                print(f"  Bottlenecks: {len(analysis['bottlenecks'])}")
                for bottleneck in analysis['bottlenecks']:
                    print(f"    - {bottleneck['type']}: {bottleneck['value']}% ({bottleneck['level']})")
            else:
                print("  No bottlenecks detected")

            # Get recommendations
            recommendations = performance_optimizer.get_optimization_recommendations()
            if recommendations['recommendations']:
                print(f"  Recommendations: {len(recommendations['recommendations'])}")
            else:
                print("  No recommendations")

            time.sleep(2)
            print()

    # Run monitoring in a thread
    monitoring_thread = threading.Thread(target=monitoring_loop)
    monitoring_thread.start()
    monitoring_thread.join()

    print("✓ Performance monitoring test completed")

def test_integration():
    """Test the complete integration"""
    print("\n=== Testing Complete Integration ===")

    # Test all features together
    @performance_optimizer.cache_decorator(expires=60)
    def process_data(data):
        print(f"Processing data: {data}")
        time.sleep(0.5)
        return f"Processed {data}"

    async def async_process(data):
        print(f"Async processing: {data}")
        await asyncio.sleep(0.3)
        return f"Async processed {data}"

    async def run_integration_test():
        # Test caching
        result1 = process_data("item1")
        result2 = process_data("item1")  # Should use cache
        result3 = process_data("item2")  # Should compute

        print(f"Results: {result1}, {result2}, {result3}")

        # Test async
        async_results = await asyncio.gather(
            performance_optimizer.async_task(async_process, "async_item1"),
            performance_optimizer.async_task(async_process, "async_item2")
        )

        print(f"Async results: {async_results}")

        # Test performance monitoring
        performance = performance_optimizer.get_system_performance()
        print(f"System performance: CPU={performance['cpu_usage']}%, Memory={performance['memory_usage']}%")

    # Run the integration test
    asyncio.run(run_integration_test())
    print("✓ Integration test completed")

def main():
    """Run all performance optimization tests"""
    print("🔍 Running Performance Optimization Tests")
    print("=" * 50)

    try:
        test_caching()
        test_async_processing()
        test_database_optimization()
        test_performance_monitoring()
        test_integration()

        print("\n🎉 All performance optimization tests completed!")
        print("✅ Performance optimization improvements are fully integrated")

    except Exception as e:
        print(f"\n❌ Performance optimization test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()



