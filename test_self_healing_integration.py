


import sys
import os
import time
import json
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.super_admin_agent import SuperAdminAgent
from agents.service_coordinator_agent import ServiceCoordinatorAgent

def test_self_healing_integration():
    """Test the integration between ServiceCoordinatorAgent and self-healing capabilities"""
    print("=== Testing Self-Healing Integration ===")

    # Initialize the agents
    admin = SuperAdminAgent()
    coordinator = ServiceCoordinatorAgent()

    # Test 1: ServiceCoordinator monitoring with self-healing
    print("\n1. Starting ServiceCoordinator monitoring...")

    # Start monitoring in a separate thread
    coordinator.start_monitoring(interval=10)

    # Give it a moment to start
    time.sleep(2)

    # Check if there are any alerts
    alerts = coordinator.alerts
    print(f"Current alerts: {len(alerts)}")

    for alert in alerts:
        print(f"  - {alert['type']}: {alert['message']}")

    # Test 2: Manual self-healing trigger
    print("\n2. Performing manual self-healing...")

    # Check system health through admin
    health_check = admin.check_self_healing()
    print(f"Health check shows {len(health_check['actions_needed'])} actions needed")

    # Perform self-healing
    if health_check['actions_needed']:
        results = admin.perform_self_healing()
        print(f"Self-healing performed {len(results['actions_taken'])} actions")

        for result in results['actions_taken']:
            print(f"  - {result['action_type']}: {result['message']}")
    else:
        print("No self-healing actions needed")

    # Test 3: Service recovery simulation
    print("\n3. Testing service recovery...")

    # Simulate a service failure
    print("Simulating service failure...")
    time.sleep(1)

    # Use self-healing to restart the service
    restart_result = admin.restart_service("test_service")
    print(f"Service restart: {restart_result['status']}")

    # If restart fails, trigger failover
    if restart_result['status'] != 'success':
        failover_result = admin.trigger_failover("test_service")
        print(f"Failover triggered: {failover_result['status']}")

    # Test 4: Resource scaling based on load
    print("\n4. Testing automatic resource scaling...")

    # Check system status
    system_status = coordinator.get_system_status()
    cpu_usage = system_status.get('system_status', {}).get('system', {}).get('cpu', {}).get('percent', 0)

    print(f"Current CPU usage: {cpu_usage}%")

    # Scale resources if needed
    if cpu_usage > 80:
        scale_result = admin.auto_scale_resources("cpu", 2)
        print(f"CPU scaling: {scale_result['status']}")
    else:
        print("CPU usage within normal range, no scaling needed")

    # Stop monitoring
    coordinator.stop_monitoring()

    print("\n=== Self-Healing Integration Test Complete ===")

if __name__ == "__main__":
    test_self_healing_integration()


