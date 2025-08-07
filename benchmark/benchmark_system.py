








import os
import sys
import time
import json
import logging
import cProfile
import pstats
import io
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.system_admin.monitoring_agent import MonitoringAgent
from agents.system_admin.logging_manager import initialize_logging
from agents.system_admin.self_healing_agent import SelfHealingAgent
from agents.system_admin.historical_analyzer import HistoricalAnalyzer

# Initialize logging
logging_manager = initialize_logging(
    service_name="BenchmarkSystem",
    environment=os.getenv('ENV', 'dev')
)

@dataclass
class BenchmarkResult:
    """Store benchmark results"""
    name: str
    duration: float
    memory_usage: float
    cpu_usage: float
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metrics: Dict[str, Any] = field(default_factory=dict)
    profile_data: Optional[str] = None

class BenchmarkSystem:
    """System for benchmarking and performance optimization"""

    def __init__(self):
        """Initialize benchmark system"""
        self.monitoring_agent = MonitoringAgent()
        self.self_healing_agent = SelfHealingAgent()
        self.historical_analyzer = HistoricalAnalyzer()
        self.results: List[BenchmarkResult] = []

    def run_benchmark(
        self,
        name: str,
        function: Callable,
        *args,
        iterations: int = 1,
        profile: bool = False,
        **kwargs
    ) -> BenchmarkResult:
        """Run a benchmark test"""
        total_duration = 0
        memory_usages = []
        cpu_usages = []

        for i in range(iterations):
            # Get initial metrics
            initial_status = self.monitoring_agent.get_current_status()
            initial_time = time.time()

            # Run the function
            if profile:
                pr = cProfile.Profile()
                pr.enable()

            result = function(*args, **kwargs)

            if profile:
                pr.disable()
                s = io.StringIO()
                ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
                ps.print_stats()
                profile_data = s.getvalue()

            # Get final metrics
            final_time = time.time()
            final_status = self.monitoring_agent.get_current_status()

            # Calculate metrics
            duration = final_time - initial_time
            memory_usage = final_status.get('memory_usage', 0) - initial_status.get('memory_usage', 0)
            cpu_usage = final_status.get('cpu_usage', 0) - initial_status.get('cpu_usage', 0)

            total_duration += duration
            memory_usages.append(memory_usage)
            cpu_usages.append(cpu_usage)

        # Calculate averages
        avg_duration = total_duration / iterations
        avg_memory = sum(memory_usages) / len(memory_usages) if memory_usages else 0
        avg_cpu = sum(cpu_usages) / len(cpu_usages) if cpu_usages else 0

        # Create result
        result = BenchmarkResult(
            name=name,
            duration=avg_duration,
            memory_usage=avg_memory,
            cpu_usage=avg_cpu,
            metrics={
                'iterations': iterations,
                'total_duration': total_duration,
                'memory_usages': memory_usages,
                'cpu_usages': cpu_usages,
                'result': result
            },
            profile_data=profile_data if profile else None
        )

        # Store result
        self.results.append(result)

        return result

    def analyze_results(self) -> Dict[str, Any]:
        """Analyze benchmark results"""
        if not self.results:
            return {"status": "no_results"}

        # Calculate averages
        avg_duration = sum(r.duration for r in self.results) / len(self.results)
        avg_memory = sum(r.memory_usage for r in self.results) / len(self.results)
        avg_cpu = sum(r.cpu_usage for r in self.results) / len(self.results)

        # Find slowest operations
        slowest = max(self.results, key=lambda r: r.duration) if self.results else None

        # Identify bottlenecks
        bottlenecks = []
        for result in self.results:
            if result.duration > avg_duration * 2:
                bottlenecks.append(result.name)

        return {
            "status": "success",
            "count": len(self.results),
            "average_duration": avg_duration,
            "average_memory": avg_memory,
            "average_cpu": avg_cpu,
            "slowest_operation": slowest.name if slowest else None,
            "slowest_duration": slowest.duration if slowest else 0,
            "bottlenecks": bottlenecks,
            "details": [r.__dict__ for r in self.results]
        }

    def generate_report(self, filename: str = "benchmark_report.json") -> str:
        """Generate benchmark report"""
        analysis = self.analyze_results()

        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "system_info": self.monitoring_agent.get_system_info(),
            "analysis": analysis,
            "results": [r.__dict__ for r in self.results]
        }

        # Save to file
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

        return filename

    def optimize_system(self) -> Dict[str, Any]:
        """Run system optimization"""
        results = []

        # Optimize resources
        resource_result = self.self_healing_agent.optimize_resources()
        results.append({"action": "optimize_resources", "result": resource_result})

        # Clear cache
        cache_result = self.self_healing_agent.clear_cache()
        results.append({"action": "clear_cache", "result": cache_result})

        # Restart critical services
        restart_result = self.self_healing_agent.restart_service("critical_service")
        results.append({"action": "restart_service", "result": restart_result})

        return {"status": "success", "optimizations": results}

    def run_stress_test(
        self,
        duration: int = 60,
        load_factor: float = 1.0,
        profile: bool = False
    ) -> Dict[str, Any]:
        """Run a stress test on the system"""
        start_time = time.time()
        end_time = start_time + duration

        metrics = []

        while time.time() < end_time:
            # Simulate load
            self._simulate_load(load_factor)

            # Get metrics
            status = self.monitoring_agent.get_current_status()
            metrics.append({
                "timestamp": datetime.utcnow().isoformat(),
                "cpu_usage": status.get('cpu_usage', 0),
                "memory_usage": status.get('memory_usage', 0),
                "disk_usage": status.get('disk_usage', 0),
                "process_count": status.get('process_count', 0)
            })

            # Small delay
            time.sleep(1)

        # Analyze results
        avg_cpu = sum(m['cpu_usage'] for m in metrics) / len(metrics) if metrics else 0
        avg_memory = sum(m['memory_usage'] for m in metrics) / len(metrics) if metrics else 0
        max_cpu = max(m['cpu_usage'] for m in metrics) if metrics else 0
        max_memory = max(m['memory_usage'] for m in metrics) if metrics else 0

        return {
            "status": "success",
            "duration": duration,
            "load_factor": load_factor,
            "average_cpu": avg_cpu,
            "average_memory": avg_memory,
            "max_cpu": max_cpu,
            "max_memory": max_memory,
            "metrics": metrics
        }

    def _simulate_load(self, load_factor: float):
        """Simulate system load"""
        # Simulate CPU load
        end_time = time.time() + 0.1 * load_factor
        while time.time() < end_time:
            # Perform some calculations
            sum(x * x for x in range(10000))

        # Simulate memory usage
        data = [x * 2 for x in range(100000)]

    def identify_bottlenecks(self) -> List[str]:
        """Identify system bottlenecks"""
        bottlenecks = []

        # Check system status
        status = self.monitoring_agent.get_current_status()

        # CPU bottleneck
        if status.get('cpu_usage', 0) > 80:
            bottlenecks.append("high_cpu_usage")

        # Memory bottleneck
        if status.get('memory_usage', 0) > 80:
            bottlenecks.append("high_memory_usage")

        # Disk bottleneck
        if status.get('disk_usage', 0) > 80:
            bottlenecks.append("high_disk_usage")

        # Process count bottleneck
        if status.get('process_count', 0) > 100:
            bottlenecks.append("high_process_count")

        return bottlenecks

    def get_optimization_recommendations(self) -> List[str]:
        """Get optimization recommendations"""
        bottlenecks = self.identify_bottlenecks()
        recommendations = []

        if "high_cpu_usage" in bottlenecks:
            recommendations.append("Optimize CPU-intensive operations")
            recommendations.append("Consider adding more CPU resources")
            recommendations.append("Implement load balancing")

        if "high_memory_usage" in bottlenecks:
            recommendations.append("Optimize memory usage")
            recommendations.append("Implement memory caching")
            recommendations.append("Consider adding more RAM")

        if "high_disk_usage" in bottlenecks:
            recommendations.append("Clean up temporary files")
            recommendations.append("Implement disk compression")
            recommendations.append("Consider adding more disk space")

        if "high_process_count" in bottlenecks:
            recommendations.append("Optimize process management")
            recommendations.append("Implement process pooling")
            recommendations.append("Reduce process creation rate")

        return recommendations

# Example usage
if __name__ == "__main__":
    benchmark = BenchmarkSystem()

    # Run some benchmarks
    def test_function(x):
        time.sleep(0.1)
        return x * 2

    result1 = benchmark.run_benchmark("Test Function", test_function, 42, iterations=5)
    print(f"Benchmark result: {result1.duration:.4f} seconds")

    # Run stress test
    stress_result = benchmark.run_stress_test(duration=10, load_factor=0.5)
    print(f"Stress test: avg CPU {stress_result['average_cpu']:.1f}%, avg Memory {stress_result['average_memory']:.1f}%")

    # Generate report
    report_file = benchmark.generate_report()
    print(f"Report generated: {report_file}")

    # Get recommendations
    recommendations = benchmark.get_optimization_recommendations()
    print("Recommendations:")
    for rec in recommendations:
        print(f"- {rec}")








