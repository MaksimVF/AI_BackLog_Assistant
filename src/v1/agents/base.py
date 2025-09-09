
from typing import Optional
from config.agent_config import get_default_model_for_agent, get_agent_registry, AgentConfig

class BaseAgent:
    def __init__(self, name=None, model_name: Optional[str] = None):
        """
        Initialize the agent.

        Args:
            name: Name of the agent (if None, uses class name)
            model_name: Specific model to use (None to use agent's default model)
        """
        self.name = name or self.__class__.__name__
        self.model_name = model_name or get_default_model_for_agent(self.name)

        # Register agent if not already registered
        registry = get_agent_registry()
        if self.name not in registry.list_agents():
            registry.register_agent(AgentConfig(
                name=self.name,
                description=f"Agent for {self.name} tasks",
                default_model=self.model_name,
                allowed_models=[]  # Will be populated from LLM config
            ))

    def log(self, message, level="info"):
        print(f"[{self.name}] [{level.upper()}] {message}")

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"

    def get_model_name(self) -> Optional[str]:
        """Get the model name this agent should use"""
        return self.model_name

    def set_model_name(self, model_name: str):
        """Set the model name this agent should use"""
        self.model_name = model_name
