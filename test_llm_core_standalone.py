


"""
Test script for standalone LLM Core functionality
"""

import sys
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from agents.llm_core_standalone import LLMCore, LLMCoreConfig, AgentCommand

def test_llm_core_standalone():
    """Test standalone LLM Core functionality"""
    print("=== Testing Standalone LLM Core ===")

    # Initialize LLM Core
    core = LLMCore(config=LLMCoreConfig(debug_mode=True))

    # Test 1: Process text command
    print("\n1. Testing process command...")
    process_command = AgentCommand(
        command_type='process',
        agent_id='test_agent',
        payload={
            'input_type': 'text',
            'data': 'Это тестовый текст для обработки через LLM Core. Он должен пройти через все этапы обработки.'
        }
    )

    response = core.process_command(process_command)
    print(f"Status: {response.status}")
    print(f"Result keys: {list(response.result.keys()) if response.result else 'None'}")

    # Test 2: Analyze text command
    print("\n2. Testing analyze command...")
    analyze_command = AgentCommand(
        command_type='analyze',
        agent_id='test_agent',
        payload={
            'text': 'Как улучшить производительность системы? Это важный вопрос для нашей команды.'
        }
    )

    response = core.process_command(analyze_command)
    print(f"Status: {response.status}")
    if response.result:
        analysis = response.result
        print(f"Context: {analysis.get('context', 'N/A')}")
        print(f"Intent: {analysis.get('intent', 'N/A')}")
        print(f"Domain tags: {analysis.get('domain_tags', [])}")
        print(f"Recommended agents: {analysis.get('recommended_agents', [])}")

    # Test 3: Route command
    print("\n3. Testing route command...")
    route_command = AgentCommand(
        command_type='route',
        agent_id='test_agent',
        payload={
            'text': 'Нам нужно срочно решить проблему с базой данных. Это критическая задача.'
        }
    )

    response = core.process_command(route_command)
    print(f"Status: {response.status}")
    if response.result:
        routing = response.result
        print(f"Next agent: {routing.get('next_agent', 'N/A')}")
        print(f"Priority: {routing.get('priority', 'N/A')}")
        print(f"Reasoning: {routing.get('reasoning', 'N/A')}")

    # Test 4: Reflect command
    print("\n4. Testing reflect command...")
    reflect_command = AgentCommand(
        command_type='reflect',
        agent_id='test_agent',
        payload={
            'text': 'Я чувствую, что наша команда не справляется с нагрузкой. Нужно что-то менять.'
        }
    )

    response = core.process_command(reflect_command)
    print(f"Status: {response.status}")
    if response.result:
        reflection = response.result.get('reflection', {})
        print(f"Context: {reflection.get('context', 'N/A')}")
        print(f"Intent: {reflection.get('intent', 'N/A')}")

        improvement_plan = response.result.get('improvement_plan')
        if improvement_plan:
            print(f"Improvement areas: {improvement_plan.get('areas_for_improvement', [])}")
            print(f"Recommended actions: {improvement_plan.get('recommended_actions', [])}")

    # Test 5: Coordinate command
    print("\n5. Testing coordinate command...")
    coordinate_command = AgentCommand(
        command_type='coordinate',
        agent_id='test_agent',
        payload={
            'agents': ['analyzer_agent', 'processor_agent'],
            'task': 'Process and analyze customer feedback data'
        }
    )

    response = core.process_command(coordinate_command)
    print(f"Status: {response.status}")
    if response.result:
        coordination = response.result
        print(f"Task: {coordination.get('task', 'N/A')}")
        print(f"Agents involved: {coordination.get('agents_involved', [])}")
        print(f"Status: {coordination.get('status', 'N/A')}")

    # Test 6: Get status and metrics
    print("\n6. Testing status and metrics...")
    status = core.get_status()
    print(f"Session ID: {status.get('session_id', 'N/A')}")
    print(f"Components: {status.get('components', {})}")

    metrics = core.get_performance_metrics()
    print(f"Total commands: {metrics['metrics'].get('total_commands', 0)}")
    print(f"Success rate: {metrics['metrics'].get('success_count', 0)}/{metrics['metrics'].get('total_commands', 1)}")
    print(f"Avg processing time: {metrics['metrics'].get('avg_processing_time', 0):.3f} seconds")

    print("\n=== All tests completed ===")

if __name__ == "__main__":
    test_llm_core_standalone()


