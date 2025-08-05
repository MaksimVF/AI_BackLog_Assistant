




"""
Test script for Service Coordinator Agent
"""

import sys
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from agents.service_coordinator_agent import ServiceCoordinatorAgent

def test_service_coordinator():
    """Test Service Coordinator Agent functionality"""
    print("=== Testing Service Coordinator Agent ===")

    with ServiceCoordinatorAgent() as coordinator:
        # Test 1: Initial system status
        print("\n1. Testing initial system status...")
        status = coordinator.get_system_status()
        print(f"   CPU usage: {status['cpu_usage']}")
        print(f"   Memory usage: {status['memory_usage']}")
        print(f"   Disk space: {status['disk_space']}")
        print(f"   System load: {status['system_load']}")
        print(f"   Active services: {status['active_services']}")

        # Test 2: Log analysis
        print("\n2. Testing log analysis...")
        log_data = """[2025-08-05 10:15:30] INFO: System started
[2025-08-05 10:16:45] WARNING: High memory usage detected
[2025-08-05 10:17:22] ERROR: Connection to database failed
[2025-08-05 10:18:10] INFO: User logged in
[2025-08-05 10:19:05] WARNING: Network latency detected
[2025-08-05 10:20:00] ERROR: Authentication failed for user"""

        analysis = coordinator.analyze_logs(log_data)
        print(f"   Total logs: {analysis['total_logs']}")
        print(f"   Error count: {analysis['error_count']}")
        print(f"   Warning count: {analysis['warning_count']}")
        print(f"   Critical issues: {analysis['critical_issues']}")
        print(f"   Recommended actions: {analysis['recommended_actions']}")

        # Test 3: Optimization recommendations
        print("\n3. Testing optimization recommendations...")
        recommendations = coordinator.get_optimization_recommendations()
        print("   Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"      {i}. {rec}")

        # Test 4: Monitoring (short test)
        print("\n4. Testing monitoring functionality...")
        coordinator.start_monitoring(interval=2)

        # Let it run for a few cycles
        start_time = time.time()
        while time.time() - start_time < 8:  # Run for about 8 seconds
            time.sleep(1)
            alerts = coordinator.get_alerts()
            if alerts:
                print(f"   🚨 Alerts detected: {len(alerts)}")
                for alert in alerts:
                    print(f"      - {alert['message']}")

        # Stop monitoring
        coordinator.stop_monitoring()
        print("   Monitoring stopped")

        # Test 5: Log buffer
        print("\n5. Testing log buffer...")
        coordinator.add_log_data("Sample log entry 1")
        coordinator.add_log_data("Sample log entry 2")
        coordinator.add_log_data("ERROR: Critical failure")

        log_buffer = coordinator.get_log_buffer()
        print(f"   Log buffer size: {len(log_buffer)}")
        print(f"   Last log entry: {log_buffer[-1] if log_buffer else 'None'}")

        # Test 6: Alert simulation
        print("\n6. Testing alert simulation...")
        # Manually create a critical condition
        coordinator.system_status.cpu_usage = "95%"
        coordinator._check_alerts()

        alerts = coordinator.get_alerts()
        if alerts:
            print(f"   🚨 Critical alerts: {len(alerts)}")
            for alert in alerts:
                print(f"      - {alert['message']}")
        else:
            print("   No alerts detected")

        print("\n=== All Service Coordinator tests completed ===")

if __name__ == "__main__":
    test_service_coordinator()




