
"""
Agent Configuration Module
Manages configuration for different agents and their LLM model assignments.
"""

from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from config.llm_config import LLMModelConfig, get_available_models

class AgentConfig(BaseModel):
    """Configuration for a specific agent"""
    name: str
    description: str = ""
    default_model: Optional[str] = None
    allowed_models: List[str] = Field(default_factory=list)
    enabled: bool = True

    class Config:
        arbitrary_types_allowed = True

class AgentRegistry:
    """Registry for managing agent configurations"""

    def __init__(self):
        """Initialize agent registry"""
        self.agents: Dict[str, AgentConfig] = {}
        self._load_default_agents()

    def _load_default_agents(self):
        """Load default agent configurations"""
        available_models = get_available_models()

        # Default agent configurations
        default_agents = [
            AgentConfig(
                name="DocumentSummarizer",
                description="Generates concise summaries of documents",
                default_model="gpt-4" if "gpt-4" in available_models else None,
                allowed_models=available_models
            ),
            AgentConfig(
                name="FactVerificationAgent",
                description="Verifies facts and statements in documents",
                default_model="claude-2" if "claude-2" in available_models else None,
                allowed_models=available_models
            ),
            AgentConfig(
                name="SentimentAnalyzer",
                description="Analyzes sentiment and tone of text",
                default_model="llama-2-7b" if "llama-2-7b" in available_models else None,
                allowed_models=available_models
            ),
            AgentConfig(
                name="CategorizationAgent",
                description="Categorizes documents and issues",
                default_model="gpt-4" if "gpt-4" in available_models else None,
                allowed_models=available_models
            ),
            AgentConfig(
                name="PrioritizationAgent",
                description="Prioritizes issues and tasks",
                default_model="claude-2" if "claude-2" in available_models else None,
                allowed_models=available_models
            )
        ]

        # Add default agents to registry
        for agent in default_agents:
            self.agents[agent.name] = agent

    def register_agent(self, agent_config: AgentConfig):
        """Register a new agent or update existing agent configuration"""
        self.agents[agent_config.name] = agent_config

    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Get configuration for a specific agent"""
        return self.agents.get(agent_name)

    def get_default_model_for_agent(self, agent_name: str) -> Optional[str]:
        """Get the default model for a specific agent"""
        agent_config = self.get_agent_config(agent_name)
        if agent_config and agent_config.default_model:
            return agent_config.default_model
        return None

    def get_allowed_models_for_agent(self, agent_name: str) -> List[str]:
        """Get allowed models for a specific agent"""
        agent_config = self.get_agent_config(agent_name)
        if agent_config:
            return agent_config.allowed_models
        return []

    def set_default_model_for_agent(self, agent_name: str, model_name: str):
        """Set the default model for a specific agent"""
        agent_config = self.get_agent_config(agent_name)
        if agent_config:
            if model_name in agent_config.allowed_models:
                agent_config.default_model = model_name
            else:
                raise ValueError(f"Model {model_name} is not allowed for agent {agent_name}")

    def list_agents(self) -> List[str]:
        """List all registered agents"""
        return list(self.agents.keys())

# Global agent registry instance
agent_registry = AgentRegistry()

def get_agent_registry() -> AgentRegistry:
    """Get the global agent registry instance"""
    return agent_registry

def get_default_model_for_agent(agent_name: str) -> Optional[str]:
    """Get the default model for a specific agent"""
    return agent_registry.get_default_model_for_agent(agent_name)

def set_default_model_for_agent(agent_name: str, model_name: str):
    """Set the default model for a specific agent"""
    agent_registry.set_default_model_for_agent(agent_name, model_name)

def register_agent(agent_config: AgentConfig):
    """Register a new agent or update existing agent configuration"""
    agent_registry.register_agent(agent_config)

def list_agents() -> List[str]:
    """List all registered agents"""
    return agent_registry.list_agents()
