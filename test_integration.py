




"""
Integration test for LLM Core and Service Coordinator Agent
"""

import sys
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from agents.llm_core_standalone import LLMCore, LLMCoreConfig, AgentCommand
from agents.service_coordinator_agent import ServiceCoordinatorAgent

def test_integration():
    """Test integration between LLM Core and Service Coordinator Agent"""
    print("=== Integration Test: LLM Core + Service Coordinator ===")

    # Initialize components
    core = LLMCore(config=LLMCoreConfig(debug_mode=True))
    coordinator = ServiceCoordinatorAgent()

    try:
        # Start service coordinator monitoring
        coordinator.start_monitoring(interval=3)

        # Test 1: System monitoring through LLM Core
        print("\n1. System monitoring through LLM Core...")
        monitor_command = AgentCommand(
            command_type='monitor_system',
            agent_id='admin_agent',
            payload={}
        )

        response = core.process_command(monitor_command)
        print(f"   Status: {response.status}")
        system_status = response.result.get('system_status', {})
        print(f"   CPU: {system_status.get('cpu_usage', 'N/A')}")
        print(f"   Memory: {system_status.get('memory_usage', 'N/A')}")
        print(f"   System load: {system_status.get('system_load', 'N/A')}")

        # Test 2: Log analysis through LLM Core
        print("\n2. Log analysis through LLM Core...")
        log_data = """[2025-08-05 10:15:30] INFO: System started
[2025-08-05 10:16:45] WARNING: High memory usage detected
[2025-08-05 10:17:22] ERROR: Connection to database failed"""

        analyze_logs_command = AgentCommand(
            command_type='analyze_logs',
            agent_id='admin_agent',
            payload={'log_data': log_data}
        )

        response = core.process_command(analyze_logs_command)
        print(f"   Status: {response.status}")
        log_analysis = response.result.get('log_analysis', {})
        print(f"   Errors: {log_analysis.get('error_count', 0)}")
        print(f"   Warnings: {log_analysis.get('warning_count', 0)}")
        print(f"   Critical issues: {log_analysis.get('critical_issues', [])}")

        # Test 3: Resource optimization through LLM Core
        print("\n3. Resource optimization through LLM Core...")
        optimize_command = AgentCommand(
            command_type='optimize_resources',
            agent_id='admin_agent',
            payload={'system_status': system_status}
        )

        response = core.process_command(optimize_command)
        print(f"   Status: {response.status}")
        recommendations = response.result.get('optimization_recommendations', [])
        print("   Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"      {i}. {rec}")

        # Test 4: Combined workflow - Monitor, Analyze, Optimize
        print("\n4. Combined workflow - Monitor, Analyze, Optimize...")

        # Step 1: Get current system status from coordinator
        current_status = coordinator.get_system_status()
        print(f"   Current CPU: {current_status['cpu_usage']}")
        print(f"   Current Memory: {current_status['memory_usage']}")

        # Step 2: Check for critical conditions
        cpu_usage = int(current_status['cpu_usage'].replace('%', ''))
        if cpu_usage > 80:
            print("   ⚠️  High CPU usage detected!")

            # Step 3: Get optimization recommendations
            optimize_response = core.process_command(optimize_command)
            recommendations = optimize_response.result.get('optimization_recommendations', [])

            print("   📋 Recommended actions:")
            for i, action in enumerate(recommendations, 1):
                print(f"      {i}. {action}")

        # Test 5: Service coordinator alerts
        print("\n5. Service coordinator alerts...")

        # Simulate a critical condition
        coordinator.system_status.cpu_usage = "95%"
        coordinator._check_alerts()

        alerts = coordinator.get_alerts()
        if alerts:
            print(f"   🚨 Critical alerts from coordinator: {len(alerts)}")
            for alert in alerts:
                print(f"      - {alert['message']}")

                # Automatically respond to alert
                if 'CPU' in alert['message']:
                    print("      🔧 Taking action: Optimizing CPU usage...")

                    # Get recommendations
                    recommendations = coordinator.get_optimization_recommendations()
                    if recommendations:
                        print(f"      📋 Suggested: {recommendations[0]}")

        # Test 6: Integration with LLM Core status
        print("\n6. Integration with LLM Core status...")
        core_status = core.get_status()
        print(f"   LLM Core session: {core_status['session_id']}")
        print(f"   Total commands: {core_status['metrics']['total_commands']}")
        print(f"   Success rate: {core_status['metrics']['success_count']}/{core_status['metrics']['total_commands']}")

        # Show how service coordinator complements LLM Core
        print("   Service coordinator provides:")
        print(f"      - System status: {coordinator.system_status.cpu_usage} CPU, {coordinator.system_status.memory_usage} Memory")
        print(f"      - Active alerts: {len(coordinator.get_alerts())}")
        print(f"      - Log buffer size: {len(coordinator.get_log_buffer())}")

        print("\n=== Integration test completed successfully ===")

    finally:
        # Clean up
        coordinator.stop_monitoring()

if __name__ == "__main__":
    test_integration()





