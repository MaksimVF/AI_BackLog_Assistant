



"""
Test script for administrative commands in LLM Core
"""

import sys
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from agents.llm_core_standalone import LLMCore, LLMCoreConfig, AgentCommand

def test_admin_commands():
    """Test administrative commands in LLM Core"""
    print("=== Testing Administrative Commands ===")

    # Initialize LLM Core
    core = LLMCore(config=LLMCoreConfig(debug_mode=True))

    # Test 1: Monitor system command
    print("\n1. Testing get_health_report command...")
    monitor_command = AgentCommand(
        command_type='get_health_report',
        agent_id='admin_agent',
        payload={}
    )

    response = core.process_command(monitor_command)
    print(f"Status: {response.status}")
    if response.result:
        system_status = response.result
        print(f"CPU usage: {system_status.get('system_status', {}).get('cpu_usage', 'N/A')}")
        print(f"Memory usage: {system_status.get('system_status', {}).get('memory_usage', 'N/A')}")
        print(f"System load: {system_status.get('system_status', {}).get('system_load', 'N/A')}")
        print(f"Active services: {system_status.get('system_status', {}).get('active_services', [])}")

    # Test 2: Run security scan command
    print("\n2. Testing run_security_scan command...")
    security_scan_command = AgentCommand(
        command_type='run_security_scan',
        agent_id='admin_agent',
        payload={}
    )

    response = core.process_command(security_scan_command)
    print(f"Status: {response.status}")
    if response.result:
        security_scan = response.result
        print(f"Security scan results: {security_scan}")

    # Test 3: Check access command
    print("\n3. Testing check_access command...")
    access_command = AgentCommand(
        command_type='check_access',
        agent_id='admin_agent',
        payload={
            'user_id': 'test_user',
            'action': 'read',
            'resource': 'sensitive_data'
        }
    )

    response = core.process_command(access_command)
    print(f"Status: {response.status}")
    if response.result:
        access_check = response.result
        print(f"Access check result: {access_check}")

    # Test 4: Combined admin workflow
    print("\n4. Testing combined admin workflow...")

    # Step 1: Get health report
    monitor_response = core.process_command(monitor_command)
    system_status = monitor_response.result

    # Step 2: Analyze based on system status
    cpu_usage = system_status.get('system_status', {}).get('system', {}).get('cpu_percent', 0)
    if cpu_usage > 80:
        print("⚠️  High CPU usage detected!")

        # Step 3: Run security scan
        security_response = core.process_command(security_scan_command)
        security_results = security_response.result

        print("🔒 Security scan results:")
        print(f"   Status: {security_results.get('status', 'N/A')}")
        print(f"   Vulnerabilities: {security_results.get('vulnerabilities_found', 0)}")

    print("\n=== All admin command tests completed ===")

if __name__ == "__main__":
    test_admin_commands()



