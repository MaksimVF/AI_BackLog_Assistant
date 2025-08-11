


"""
Test script for agent configuration system.
"""

from config.agent_config import (
    get_agent_registry,
    set_default_model_for_agent,
    register_agent,
    AgentConfig
)

def test_agent_config():
    """Test agent configuration system"""
    print("Testing agent configuration system...")
    print()

    # Test 1: Get registry and list agents
    registry = get_agent_registry()
    agents = registry.list_agents()
    print(f"Available agents: {agents}")
    print()

    # Test 2: Get agent configurations
    for agent_name in agents:
        config = registry.get_agent_config(agent_name)
        print(f"Agent: {agent_name}")
        print(f"  Description: {config.description}")
        print(f"  Default model: {config.default_model}")
        print(f"  Allowed models: {config.allowed_models}")
        print()

    # Test 3: Set default model for an agent
    print("Setting default model for DocumentSummarizer to 'claude-2'")
    set_default_model_for_agent("DocumentSummarizer", "claude-2")
    updated_config = registry.get_agent_config("DocumentSummarizer")
    print(f"Updated default model: {updated_config.default_model}")
    print()

    # Test 4: Register a new agent
    print("Registering a new agent type...")
    new_agent = AgentConfig(
        name="TestAgent",
        description="Agent for testing purposes",
        default_model="llama-2-7b",
        allowed_models=["llama-2-7b", "gpt-4"]
    )
    register_agent(new_agent)

    # Verify registration
    test_config = registry.get_agent_config("TestAgent")
    print(f"New agent registered: {test_config.name}")
    print(f"  Description: {test_config.description}")
    print(f"  Default model: {test_config.default_model}")
    print()

    # Test 5: List agents again to verify new agent
    updated_agents = registry.list_agents()
    print(f"Updated agent list: {updated_agents}")
    print(f"TestAgent found: {'TestAgent' in updated_agents}")
    print()

    print("All tests completed successfully!")

if __name__ == "__main__":
    test_agent_config()


