



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
    print("\n1. Testing monitor_system command...")
    monitor_command = AgentCommand(
        command_type='monitor_system',
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

    # Test 2: Analyze logs command
    print("\n2. Testing analyze_logs command...")
    log_data = """[2025-08-05 10:15:30] INFO: System started
[2025-08-05 10:16:45] WARNING: High memory usage detected
[2025-08-05 10:17:22] ERROR: Connection to database failed
[2025-08-05 10:18:10] INFO: User logged in"""

    analyze_logs_command = AgentCommand(
        command_type='analyze_logs',
        agent_id='admin_agent',
        payload={
            'log_data': log_data
        }
    )

    response = core.process_command(analyze_logs_command)
    print(f"Status: {response.status}")
    if response.result:
        log_analysis = response.result.get('log_analysis', {})
        print(f"Total logs: {log_analysis.get('total_logs', 0)}")
        print(f"Error count: {log_analysis.get('error_count', 0)}")
        print(f"Warning count: {log_analysis.get('warning_count', 0)}")
        print(f"Critical issues: {log_analysis.get('critical_issues', [])}")
        print(f"Recommended actions: {log_analysis.get('recommended_actions', [])}")

    # Test 3: Optimize resources command
    print("\n3. Testing optimize_resources command...")
    optimize_command = AgentCommand(
        command_type='optimize_resources',
        agent_id='admin_agent',
        payload={
            'system_status': {
                'cpu_usage': '85%',
                'memory_usage': '70%',
                'disk_space': '50% free'
            }
        }
    )

    response = core.process_command(optimize_command)
    print(f"Status: {response.status}")
    if response.result:
        optimization = response.result
        print(f"Recommendations: {optimization.get('optimization_recommendations', [])}")
        print(f"Message: {optimization.get('message', 'N/A')}")

    # Test 4: Combined admin workflow
    print("\n4. Testing combined admin workflow...")

    # Step 1: Monitor system
    monitor_response = core.process_command(monitor_command)
    system_status = monitor_response.result.get('system_status', {})

    # Step 2: Analyze based on system status
    if system_status.get('cpu_usage', '0%') > '80%':
        print("⚠️  High CPU usage detected!")

        # Step 3: Get optimization recommendations
        optimize_response = core.process_command(optimize_command)
        recommendations = optimize_response.result.get('optimization_recommendations', [])

        print("📋 Recommended actions:")
        for i, action in enumerate(recommendations, 1):
            print(f"   {i}. {action}")

    print("\n=== All admin command tests completed ===")

if __name__ == "__main__":
    test_admin_commands()



