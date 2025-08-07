



import sys
import os
import time
import json
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.system_admin.self_healing_agent import SelfHealingAgent
from agents.system_admin.config_manager import ConfigManager

def test_config_management():
    """Test the enhanced configuration management capabilities"""
    print("=== Testing Configuration Management ===")

    # Test 1: Initialize with default config
    print("\n1. Testing default configuration...")
    agent = SelfHealingAgent()
    print(f"Default thresholds: {agent.thresholds}")

    # Test 2: Update configuration dynamically
    print("\n2. Testing dynamic configuration update...")
    new_config = {
        'cpu_critical': 80.0,
        'memory_critical': 80.0,
        'disk_critical': 75.0
    }
    agent.update_config(new_config)
    print(f"Updated thresholds: {agent.thresholds}")

    # Test 3: Load configuration from file
    print("\n3. Testing configuration loading from file...")
    success = agent.load_config_from_file('config.dev.yaml')
    print(f"Loaded from config.dev.yaml: {success}")
    print(f"New thresholds: {agent.thresholds}")

    # Test 4: Environment-specific configuration
    print("\n4. Testing environment-specific configuration...")
    os.environ['ENV'] = 'test'
    agent_test = SelfHealingAgent()
    print(f"Test environment thresholds: {agent_test.thresholds}")

    os.environ['ENV'] = 'prod'
    agent_prod = SelfHealingAgent()
    print(f"Production environment thresholds: {agent_prod.thresholds}")

    # Test 5: Configuration sources
    print("\n5. Testing configuration sources...")
    print(f"Config sources: {agent.config_manager.get_config_sources()}")

    # Test 6: Configuration validation
    print("\n6. Testing configuration validation...")
    try:
        invalid_config = {
            'cpu_critical': 120.0,  # Invalid value > 100
            'cache_cleanup_interval': -1  # Invalid negative value
        }
        agent.update_config(invalid_config)
    except Exception as e:
        print(f"Validation error caught: {e}")

    print("\n=== Configuration Management Test Complete ===")

if __name__ == "__main__":
    test_config_management()



