

import sys
import os
import time
import json
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.super_admin_agent import SuperAdminAgent

def test_self_healing():
    """Test the self-healing capabilities of the system"""
    print("=== Testing Self-Healing Capabilities ===")

    # Initialize the admin agent
    admin = SuperAdminAgent()

    # Test 1: Check system health
    print("\n1. Checking system health...")
    health_check = admin.check_self_healing()
    print(f"Health check completed at: {health_check.get('timestamp')}")
    print(f"Actions needed: {len(health_check.get('actions_needed', []))}")

    for action in health_check.get('actions_needed', []):
        print(f"  - {action['type']} ({action['priority']}): {action['details']}")

    # Test 2: Perform self-healing
    print("\n2. Performing self-healing actions...")
    if health_check.get('actions_needed'):
        healing_results = admin.perform_self_healing()
        print(f"Actions taken: {len(healing_results.get('actions_taken', []))}")

        for result in healing_results.get('actions_taken', []):
            print(f"  - {result['action_type']}: {result.get('message', 'No details')}")
    else:
        print("No self-healing actions needed")

    # Test 3: Service restart
    print("\n3. Testing service restart...")
    service_result = admin.restart_service("test_service")
    print(f"Service restart result: {service_result['status']}")
    print(f"Message: {service_result['message']}")

    # Test 4: Failover
    print("\n4. Testing failover...")
    failover_result = admin.trigger_failover("database_service")
    print(f"Failover result: {failover_result['status']}")
    print(f"Message: {failover_result['message']}")

    # Test 5: Auto-scaling
    print("\n5. Testing auto-scaling...")
    scale_result = admin.auto_scale_resources("memory", 4)
    print(f"Auto-scale result: {scale_result['status']}")
    print(f"Message: {scale_result['message']}")

    print("\n=== Self-Healing Test Complete ===")

if __name__ == "__main__":
    test_self_healing()

