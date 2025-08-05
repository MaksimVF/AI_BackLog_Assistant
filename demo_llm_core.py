


"""
LLM Core Demo - Interactive demonstration of LLM Core capabilities
"""

import sys
import json
import logging
from agents.llm_core_standalone import LLMCore, LLMCoreConfig, AgentCommand

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_result(title, result):
    """Print a formatted result"""
    print(f"\n📊 {title}:")
    print("-" * 40)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("-" * 40)

def demo_llm_core():
    """Interactive demo of LLM Core capabilities"""

    print_header("LLM Core Interactive Demo")
    print("Welcome to the LLM Core demonstration!")
    print("This demo shows the core capabilities of the AI system.")

    # Initialize LLM Core
    core = LLMCore(config=LLMCoreConfig(debug_mode=False))
    print(f"\n✅ LLM Core initialized (Session: {core.session_id})")

    # Demo 1: Text Processing
    print_header("1. Text Processing")
    print("Processing a sample text document...")

    process_command = AgentCommand(
        command_type='process',
        agent_id='demo_agent',
        payload={
            'input_type': 'text',
            'data': 'Это важный документ, который нужно обработать и проанализировать. Он содержит информацию о проекте и задачах.'
        }
    )

    response = core.process_command(process_command)
    print_result("Processing Result", response.result)

    # Demo 2: Text Analysis
    print_header("2. Text Analysis")
    print("Analyzing a complex question...")

    analyze_command = AgentCommand(
        command_type='analyze',
        agent_id='demo_agent',
        payload={
            'text': 'Как мы можем оптимизировать процессы в нашей компании для повышения эффективности?'
        }
    )

    response = core.process_command(analyze_command)
    print_result("Analysis Result", response.result)

    # Demo 3: Routing
    print_header("3. Intelligent Routing")
    print("Determining the best agent to handle a task...")

    route_command = AgentCommand(
        command_type='route',
        agent_id='demo_agent',
        payload={
            'text': 'Нам нужно срочно проанализировать этот контракт и выделить ключевые пункты'
        }
    )

    response = core.process_command(route_command)
    print_result("Routing Result", response.result)

    # Demo 4: Reflection and Self-Improvement
    print_header("4. Reflection and Self-Improvement")
    print("Performing self-reflection on system performance...")

    reflect_command = AgentCommand(
        command_type='reflect',
        agent_id='demo_agent',
        payload={
            'text': 'Система часто ошибается в классификации профессиональных вопросов. Нужно улучшить точность.'
        }
    )

    response = core.process_command(reflect_command)
    print_result("Reflection Result", response.result)

    # Demo 5: Coordination
    print_header("5. Multi-Agent Coordination")
    print("Coordinating multiple agents for a complex task...")

    coordinate_command = AgentCommand(
        command_type='coordinate',
        agent_id='demo_agent',
        payload={
            'agents': ['analyzer_agent', 'processor_agent', 'validator_agent'],
            'task': 'Process and validate customer feedback data from multiple sources'
        }
    )

    response = core.process_command(coordinate_command)
    print_result("Coordination Result", response.result)

    # Demo 6: Performance Metrics
    print_header("6. Performance Monitoring")
    print("Checking system performance and health...")

    status = core.get_status()
    metrics = core.get_performance_metrics()

    print("\n📈 System Status:")
    print(f"   Session ID: {status['session_id']}")
    print(f"   Commands Processed: {metrics['metrics']['total_commands']}")
    print(f"   Success Rate: {metrics['metrics']['success_count']}/{metrics['metrics']['total_commands']}")
    print(f"   Avg Processing Time: {metrics['metrics']['avg_processing_time']:.3f} seconds")
    print(f"   Components Active: {len(status['components'])}")

    # Demo 7: Command History
    print_header("7. Command History")
    print("Reviewing recent commands...")

    print(f"\n🕒 Command History (last {len(core.command_history)} commands):")
    for i, cmd in enumerate(core.command_history[-3:], 1):
        print(f"   {i}. {cmd['command']['command_type']} - {cmd['command']['payload'].get('text', 'N/A')[:50]}...")

    # Conclusion
    print_header("Demo Complete")
    print("🎉 Thank you for using the LLM Core Demo!")
    print("\nKey capabilities demonstrated:")
    print("✅ Text processing and analysis")
    print("✅ Intelligent routing")
    print("✅ Self-reflection and improvement")
    print("✅ Multi-agent coordination")
    print("✅ Performance monitoring")
    print("✅ Command history tracking")

    print("\nThe LLM Core provides a powerful foundation for building")
    print("intelligent agent systems with advanced cognitive capabilities.")

if __name__ == "__main__":
    demo_llm_core()



