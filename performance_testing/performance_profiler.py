


"""
Performance Profiler

Comprehensive performance testing and profiling tools for the AI BackLog Assistant.
"""

import time
import threading
import queue
import psutil
import os
from typing import Callable, List, Dict, Any, Optional
from dataclasses import dataclass
import json
import csv
from contextlib import contextmanager

@dataclass
class PerformanceMetrics:
    """Performance metrics for a single test run"""
    test_name: str
    duration: float  # seconds
    request_count: int
    success_count: int
    error_count: int
    avg_latency: float  # ms
    min_latency: float  # ms
    max_latency: float  # ms
    throughput: float  # requests per second
    cpu_usage: float  # average %
    memory_usage: float  # average MB
    timestamp: float

class PerformanceProfiler:
    """
    Performance profiler for testing system components.

    Features:
    - Throughput and latency measurement
    - Resource usage monitoring (CPU, memory)
    - Concurrent load testing
    - Detailed reporting
    """

    def __init__(self):
        self.results = []
        self._resource_monitor = None
        self._resource_data = []
        self._resource_monitor_thread = None
        self._stop_monitoring = threading.Event()

    def _monitor_resources(self, interval=0.1):
        """Monitor CPU and memory usage"""
        process = psutil.Process(os.getpid())

        while not self._stop_monitoring.is_set():
            try:
                # Get CPU and memory usage
                cpu_percent = process.cpu_percent(interval=0)
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024

                self._resource_data.append({
                    'timestamp': time.time(),
                    'cpu_percent': cpu_percent,
                    'memory_mb': memory_mb
                })

                time.sleep(interval)
            except Exception as e:
                print(f"Resource monitoring error: {e}")
                break

    @contextmanager
    def monitor_resources(self):
        """Context manager for resource monitoring"""
        self._stop_monitoring.clear()
        self._resource_data = []

        # Start resource monitoring thread
        self._resource_monitor_thread = threading.Thread(
            target=self._monitor_resources,
            daemon=True
        )
        self._resource_monitor_thread.start()

        try:
            yield
        finally:
            # Stop monitoring
            self._stop_monitoring.set()
            self._resource_monitor_thread.join(timeout=1.0)

    def _calculate_resource_usage(self, duration):
        """Calculate average resource usage over test duration"""
        if not self._resource_data:
            return 0.0, 0.0

        # Filter data for the test duration window
        end_time = time.time()
        start_time = end_time - duration

        filtered_data = [
            d for d in self._resource_data
            if start_time <= d['timestamp'] <= end_time
        ]

        if not filtered_data:
            return 0.0, 0.0

        avg_cpu = sum(d['cpu_percent'] for d in filtered_data) / len(filtered_data)
        avg_memory = sum(d['memory_mb'] for d in filtered_data) / len(filtered_data)

        return avg_cpu, avg_memory

    def run_test(
        self,
        test_name: str,
        test_function: Callable,
        duration: float = 5.0,
        concurrency: int = 1,
        warmup: float = 1.0,
        **kwargs
    ) -> PerformanceMetrics:
        """
        Run a performance test.

        Args:
            test_name: Name of the test
            test_function: Function to test (should accept **kwargs)
            duration: Test duration in seconds
            concurrency: Number of concurrent threads
            warmup: Warmup time before measurement
            **kwargs: Arguments to pass to test_function

        Returns:
            PerformanceMetrics object
        """

        # Warmup
        if warmup > 0:
            print(f"Warming up for {warmup:.1f}s...")
            end_time = time.time() + warmup
            while time.time() < end_time:
                try:
                    test_function(**kwargs)
                except:
                    pass

        print(f"Running test: {test_name} (duration: {duration}s, concurrency: {concurrency})")

        # Prepare for test
        latencies = []
        success_count = 0
        error_count = 0
        request_count = 0
        result_queue = queue.Queue()

        def worker():
            """Worker function for concurrent testing"""
            nonlocal request_count, success_count, error_count

            while time.time() < end_time:
                start_time = time.time()
                try:
                    result = test_function(**kwargs)
                    result_queue.put((True, result, start_time))
                    success_count += 1
                except Exception as e:
                    result_queue.put((False, str(e), start_time))
                    error_count += 1
                request_count += 1

        # Start resource monitoring
        with self.monitor_resources():
            # Run test
            end_time = time.time() + duration
            threads = []

            for _ in range(concurrency):
                t = threading.Thread(target=worker, daemon=True)
                t.start()
                threads.append(t)

            # Wait for threads to complete
            for t in threads:
                t.join(timeout=duration + 1)

        # Process results
        while not result_queue.empty():
            success, result, start_time = result_queue.get()
            latency = (time.time() - start_time) * 1000  # Convert to ms
            latencies.append(latency)

        # Calculate metrics
        test_duration = duration  # We use the intended duration
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        min_latency = min(latencies) if latencies else 0
        max_latency = max(latencies) if latencies else 0
        throughput = request_count / test_duration

        # Calculate resource usage
        avg_cpu, avg_memory = self._calculate_resource_usage(test_duration)

        # Create metrics object
        metrics = PerformanceMetrics(
            test_name=test_name,
            duration=test_duration,
            request_count=request_count,
            success_count=success_count,
            error_count=error_count,
            avg_latency=avg_latency,
            min_latency=min_latency,
            max_latency=max_latency,
            throughput=throughput,
            cpu_usage=avg_cpu,
            memory_usage=avg_memory,
            timestamp=time.time()
        )

        self.results.append(metrics)
        return metrics

    def save_results(self, filename: str, format: str = 'json'):
        """Save performance test results"""
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump([vars(r) for r in self.results], f, indent=2)
        elif format == 'csv':
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write header
                header = list(vars(self.results[0]).keys()) if self.results else []
                writer.writerow(header)
                # Write data
                for result in self.results:
                    writer.writerow(vars(result).values())
        else:
            raise ValueError(f"Unsupported format: {format}")

    def print_summary(self):
        """Print summary of all test results"""
        if not self.results:
            print("No test results available")
            return

        print("\n" + "="*80)
        print("PERFORMANCE TEST SUMMARY")
        print("="*80)

        for i, result in enumerate(self.results, 1):
            print(f"\nTest {i}: {result.test_name}")
            print(f"  Duration: {result.duration:.1f}s")
            print(f"  Requests: {result.request_count}")
            print(f"  Success: {result.success_count}")
            print(f"  Errors: {result.error_count}")
            print(f"  Throughput: {result.throughput:.1f} req/s")
            print(f"  Avg Latency: {result.avg_latency:.1f} ms")
            print(f"  Min Latency: {result.min_latency:.1f} ms")
            print(f"  Max Latency: {result.max_latency:.1f} ms")
            print(f"  CPU Usage: {result.cpu_usage:.1f} %")
            print(f"  Memory Usage: {result.memory_usage:.1f} MB")

        print("\n" + "="*80)

# Example usage
if __name__ == "__main__":
    def sample_function(x):
        """Sample function for testing"""
        time.sleep(0.1)  # Simulate work
        return x * 2

    profiler = PerformanceProfiler()

    # Run a simple test
    profiler.run_test(
        "Sample Function Test",
        sample_function,
        duration=3,
        concurrency=2,
        x=5
    )

    # Print results
    profiler.print_summary()

    # Save results
    profiler.save_results("test_results.json")


