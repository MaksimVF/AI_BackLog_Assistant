

# Agent-Specific LLM Model Configuration

## Overview

This implementation enables different agents to work with different LLM models, providing flexibility in model selection and allowing optimization of each agent's performance based on the strengths of different models.

## Key Features

1. **Per-Agent Model Configuration**: Each agent can be configured to use a specific LLM model by default
2. **Runtime Model Override**: Agents can override their default model at runtime for specific tasks
3. **Dynamic Configuration**: Agent model configurations can be changed programmatically
4. **Fallback Support**: Agents gracefully handle cases where their preferred model is unavailable

## Implementation Components

### 1. Agent Configuration System (`config/agent_config.py`)

The agent configuration system manages:
- Default model assignments for each agent
- Allowed models for each agent
- Agent registration and discovery

### 2. Enhanced Base Agent (`agents/base.py`)

The `BaseAgent` class now includes:
- Model name management
- Automatic model configuration based on agent type
- Methods to get/set the current model

### 3. LLM Client Enhancements (`agents/llm_client.py`)

The LLM client functions (`chat_completion`, `text_completion`) now accept:
- Optional `agent` parameter to automatically use the agent's configured model
- Backward compatibility with existing code

## Usage Examples

### 1. Creating Agents with Different Models

```python
# Create agent with default model for its type
summarizer = DocumentSummarizer()

# Create agent with specific model
analyzer = SentimentAnalyzer(model_name="claude-2")

# Change an agent's model at runtime
summarizer.set_model_name("llama-2-7b")
```

### 2. Using Agents with LLM Calls

```python
# Use agent's default model
response = chat_completion(messages, agent=summarizer)

# Override model for a specific call
response = chat_completion(messages, model_name="gpt-4", agent=summarizer)

# Traditional usage (without agent parameter)
response = chat_completion(messages, model_name="gpt-4")
```

### 3. Configuration Management

```python
from config.agent_config import (
    get_agent_registry,
    set_default_model_for_agent,
    register_agent,
    AgentConfig
)

# Get available agents
agents = get_agent_registry().list_agents()

# Set default model for an agent type
set_default_model_for_agent("DocumentSummarizer", "claude-2")

# Register a new agent type
register_agent(AgentConfig(
    name="CustomAgent",
    description="Agent for custom tasks",
    default_model="gpt-4",
    allowed_models=["gpt-4", "claude-2", "llama-2-7b"]
))
```

## Benefits

1. **Optimized Performance**: Assign models based on their strengths (e.g., summarization, analysis, creativity)
2. **Cost Management**: Use less expensive models for simpler tasks
3. **Flexibility**: Easily switch models for experimentation or A/B testing
4. **Resilience**: Automatic fallback when preferred models are unavailable

## Configuration

Agent configurations are managed in `config/agent_config.py`. The default configuration includes:

- DocumentSummarizer: Default model "gpt-4"
- FactVerificationAgent: Default model "claude-2"
- SentimentAnalyzer: Default model "llama-2-7b"
- CategorizationAgent: Default model "gpt-4"
- PrioritizationAgent: Default model "claude-2"

## Testing

The implementation includes demonstration scripts:

- `test_agent_models.py`: Tests the actual LLM integration (requires API keys)
- `demo_agent_models.py`: Mock demonstration showing the concept without API calls

## Future Enhancements

1. **Model Performance Tracking**: Monitor and automatically adjust model assignments
2. **Cost-Based Routing**: Optimize model selection based on usage costs
3. **Model Capability Registry**: Track and utilize specific capabilities of each model
4. **Adaptive Fallback**: Intelligent fallback strategies based on task requirements

## Implementation Notes

- The system maintains backward compatibility with existing agent implementations
- Agents can be configured to use any available model from the LLM configuration
- Model assignments can be changed at runtime without restarting the system
- The configuration system supports both static configuration and dynamic updates

