


"""
Test script for enhanced system monitoring and real metrics integration
"""

import time
import json
from agents.service_coordinator_agent import ServiceCoordinatorAgent

def test_enhanced_monitoring():
    """Test the enhanced monitoring functionality"""
    print("=== Testing Enhanced System Monitoring ===")

    with ServiceCoordinatorAgent() as coordinator:
        # Start monitoring
        coordinator.start_monitoring(interval=5)

        try:
            # Get initial status
            print("\n1. Comprehensive System Status:")
            status = coordinator.get_system_status()
            print(json.dumps(status, indent=2, default=str))

            # Test enhanced log analysis
            print("\n2. Enhanced Log Analysis:")
            log_data = """[2025-08-06 14:22:30] INFO: System started successfully
[2025-08-06 14:23:15] WARNING: High memory usage detected in process 4567
[2025-08-06 14:24:05] ERROR: Database connection timeout
[2025-08-06 14:25:20] ERROR: Memory leak detected in application
[2025-08-06 14:26:45] CRITICAL: System load exceeds safe limits
[2025-08-06 14:27:30] WARNING: Network latency above threshold
[2025-08-06 14:28:10] INFO: User login successful"""

            analysis = coordinator.analyze_logs(log_data)
            print("Log Analysis Results:")
            print(f"  Total logs: {analysis['total_logs']}")
            print(f"  Errors: {analysis['error_count']}")
            print(f"  Warnings: {analysis['warning_count']}")
            print(f"  Critical: {analysis['critical_count']}")
            print(f"  Error patterns: {analysis['error_patterns']}")
            print(f"  Warning patterns: {analysis['warning_patterns']}")
            print(f"  Critical issues: {analysis['critical_issues']}")
            print(f"  Recommendations: {analysis['recommended_actions']}")

            # Test optimization recommendations
            print("\n3. Comprehensive Optimization Recommendations:")
            recommendations = coordinator.get_optimization_recommendations()
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")

            # Let monitoring run and check alerts
            print("\n4. Monitoring and Alerts:")
            for i in range(3):
                time.sleep(2)
                alerts = coordinator.get_alerts()
                if alerts:
                    print(f"   Monitoring cycle {i+1}: {len(alerts)} alerts detected")
                    for alert in alerts:
                        print(f"     - [{alert['type']}] {alert['message']}")
                else:
                    print(f"   Monitoring cycle {i+1}: No alerts")

        except KeyboardInterrupt:
            print("\nTest interrupted by user")

    print("\n=== Enhanced Monitoring Test Completed ===")

if __name__ == "__main__":
    test_enhanced_monitoring()


