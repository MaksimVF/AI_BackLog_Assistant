








import os
import sys
import time
import unittest
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmark.benchmark_system import BenchmarkSystem, BenchmarkResult

class TestBenchmarkSystem(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.benchmark = BenchmarkSystem()

    def test_run_benchmark(self):
        """Test benchmark execution"""
        def test_function(x):
            time.sleep(0.01)
            return x * 2

        result = self.benchmark.run_benchmark("Test Function", test_function, 42, iterations=3)

        # Verify result
        self.assertIsInstance(result, BenchmarkResult)
        self.assertEqual(result.name, "Test Function")
        self.assertGreater(result.duration, 0)
        self.assertTrue(0 <= result.duration <= 1)  # Should be around 0.03 seconds

    def test_analyze_results(self):
        """Test result analysis"""
        # Add some mock results
        self.benchmark.results = [
            BenchmarkResult(name="Fast Function", duration=0.01, memory_usage=10, cpu_usage=5),
            BenchmarkResult(name="Slow Function", duration=0.1, memory_usage=20, cpu_usage=10),
            BenchmarkResult(name="Medium Function", duration=0.05, memory_usage=15, cpu_usage=7)
        ]

        analysis = self.benchmark.analyze_results()

        # Verify analysis
        self.assertEqual(analysis["status"], "success")
        self.assertEqual(analysis["count"], 3)
        self.assertEqual(analysis["slowest_operation"], "Slow Function")
        self.assertEqual(analysis["bottlenecks"], ["Slow Function"])

    def test_generate_report(self):
        """Test report generation"""
        # Add a mock result
        self.benchmark.results = [
            BenchmarkResult(name="Test Function", duration=0.01, memory_usage=10, cpu_usage=5)
        ]

        # Generate report
        report_file = self.benchmark.generate_report("test_report.json")

        # Verify file exists
        self.assertTrue(os.path.exists(report_file))

        # Clean up
        os.remove(report_file)

    @patch('benchmark.benchmark_system.SelfHealingAgent')
    def test_optimize_system(self, MockSelfHealingAgent):
        """Test system optimization"""
        # Mock self-healing agent
        mock_agent = MockSelfHealingAgent.return_value
        mock_agent.optimize_resources.return_value = "Resources optimized"
        mock_agent.clear_cache.return_value = "Cache cleared"
        mock_agent.restart_service.return_value = "Service restarted"

        # Run optimization
        result = self.benchmark.optimize_system()

        # Verify result
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["optimizations"]), 3)

    def test_stress_test(self):
        """Test stress testing"""
        # Run a short stress test
        result = self.benchmark.run_stress_test(duration=2, load_factor=0.1)

        # Verify result
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["duration"], 2)
        self.assertGreaterEqual(result["average_cpu"], 0)
        self.assertGreaterEqual(result["average_memory"], 0)

    def test_identify_bottlenecks(self):
        """Test bottleneck identification"""
        # Mock monitoring agent
        with patch.object(self.benchmark.monitoring_agent, 'get_current_status') as mock_status:
            mock_status.return_value = {
                "cpu_usage": 85,
                "memory_usage": 75,
                "disk_usage": 60,
                "process_count": 50
            }

            bottlenecks = self.benchmark.identify_bottlenecks()

            # Verify bottlenecks
            self.assertIn("high_cpu_usage", bottlenecks)
            self.assertNotIn("high_memory_usage", bottlenecks)
            self.assertNotIn("high_disk_usage", bottlenecks)
            self.assertNotIn("high_process_count", bottlenecks)

    def test_get_optimization_recommendations(self):
        """Test optimization recommendations"""
        # Mock bottlenecks
        with patch.object(self.benchmark, 'identify_bottlenecks') as mock_bottlenecks:
            mock_bottlenecks.return_value = ["high_cpu_usage", "high_memory_usage"]

            recommendations = self.benchmark.get_optimization_recommendations()

            # Verify recommendations
            self.assertGreater(len(recommendations), 0)
            self.assertIn("Optimize CPU-intensive operations", recommendations)
            self.assertIn("Optimize memory usage", recommendations)

if __name__ == "__main__":
    unittest.main()









