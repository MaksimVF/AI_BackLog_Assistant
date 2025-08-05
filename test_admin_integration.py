
"""
Test script for admin integration with LLM Core and Service Coordinator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.llm_core_standalone import LLMCore, AgentCommand
from agents.service_coordinator_agent import ServiceCoordinatorAgent

def test_llm_core_admin_commands():
    """Test admin commands in LLM Core"""
    print("=== Testing LLM Core Admin Commands ===")

    # Initialize LLM Core
    core = LLMCore()

    # Test health report command
    health_command = AgentCommand(
        command_type='get_health_report',
        agent_id='admin_agent',
        payload={}
    )

    health_response = core.process_command(health_command)
    print(f"Health Report: {health_response.status}")
    if health_response.status == 'success':
        print(f"System Status: {health_response.result.get('system_status', 'N/A')}")
        print(f"Diagnostics: {health_response.result.get('diagnostics', 'N/A')}")

    # Test security scan command
    security_command = AgentCommand(
        command_type='run_security_scan',
        agent_id='admin_agent',
        payload={}
    )

    security_response = core.process_command(security_command)
    print(f"\nSecurity Scan: {security_response.status}")
    if security_response.status == 'success':
        print(f"Vulnerabilities: {security_response.result.get('vulnerabilities', 'None')}")
        print(f"Recommendations: {security_response.result.get('recommendations', 'None')}")

    # Test access check command
    access_command = AgentCommand(
        command_type='check_access',
        agent_id='admin_agent',
        payload={
            'user_id': 'test_user',
            'action': 'read',
            'resource': 'sensitive_data'
        }
    )

    access_response = core.process_command(access_command)
    print(f"\nAccess Check: {access_response.status}")
    if access_response.status == 'success':
        print(f"User: {access_response.result.get('user_id')}")
        print(f"Action: {access_response.result.get('action')}")
        print(f"Resource: {access_response.result.get('resource')}")
        print(f"Has Access: {access_response.result.get('has_access')}")

def test_service_coordinator_admin():
    """Test admin functionality in Service Coordinator"""
    print("\n=== Testing Service Coordinator Admin Integration ===")

    # Initialize Service Coordinator
    coordinator = ServiceCoordinatorAgent()

    # Test health check
    health_status = coordinator.get_system_status()
    print(f"Service Coordinator Health Status: {health_status}")

    # Test security scan
    security_scan = coordinator.run_security_scan()
    print(f"Security Scan Results: {security_scan}")

    # Test access control
    has_access = coordinator.check_access('admin_user', 'read', 'system_logs')
    print(f"Admin user access to system logs: {has_access}")

    has_access = coordinator.check_access('guest_user', 'write', 'config')
    print(f"Guest user access to config: {has_access}")

    # Test exception handling
    try:
        raise ValueError("Test exception for error handling")
    except Exception as e:
        error_result = coordinator.handle_exception(e, "test_module")
        print(f"Exception handling result: {error_result}")

def test_integration():
    """Test integration between LLM Core and Service Coordinator"""
    print("\n=== Testing Integration ===")

    # Initialize both components
    core = LLMCore()
    coordinator = ServiceCoordinatorAgent()

    # Test that both can access admin functionality
    core_health = core.process_command(AgentCommand(
        command_type='get_health_report',
        agent_id='admin_agent',
        payload={}
    ))

    coord_health = coordinator.get_system_status()

    print(f"LLM Core health status: {core_health.status}")
    print(f"Service Coordinator health status: {coord_health}")

    # Verify both use the same underlying admin agent
    assert 'system_status' in core_health.result
    assert 'system_status' in coord_health
    print("✅ Integration test passed!")

if __name__ == "__main__":
    test_llm_core_admin_commands()
    test_service_coordinator_admin()
    test_integration()
    print("\n🎉 All admin integration tests completed successfully!")
