


from typing import List, Dict, Any, Optional
import logging
from .base_infra_agent import BaseInfraAgent
from .weaviate_checker import WeaviateCheckerAgent
from .queue_checker import QueueCheckerAgent
from .llm_checker import LLMCheckerAgent
from .system_monitor import SystemMonitorAgent
from .config_checker import ConfigCheckerAgent

logger = logging.getLogger("InfraAgent")

class InfrastructureAgent:
    """Main infrastructure monitoring and management agent."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.sub_agents: List[BaseInfraAgent] = []
        self.status = "initializing"
        self.initialize_sub_agents()

    def initialize_sub_agents(self) -> None:
        """Initialize all sub-agents."""
        sub_agents_config = self.config.get("sub_agents", {})

        # Initialize sub-agents with their specific configurations
        self.sub_agents = [
            WeaviateCheckerAgent(config=sub_agents_config.get("weaviate", {})),
            QueueCheckerAgent(config=sub_agents_config.get("queue", {})),
            LLMCheckerAgent(config=sub_agents_config.get("llm", {})),
            SystemMonitorAgent(config=sub_agents_config.get("system", {})),
            ConfigCheckerAgent(config=sub_agents_config.get("config", {}))
        ]
        self.status = "ready"
        logger.info("All sub-agents initialized")

    def run_full_check(self) -> Dict[str, Any]:
        """Run a full infrastructure check."""
        results = {}
        for agent in self.sub_agents:
            results[agent.name] = agent.run_check()
        return results

    def get_status(self) -> Dict[str, Any]:
        """Get overall infrastructure status."""
        status = {
            "status": self.status,
            "sub_agents": {agent.name: agent.get_status() for agent in self.sub_agents}
        }
        return status

    def get_sub_agent(self, name: str) -> Optional[BaseInfraAgent]:
        """Get a specific sub-agent by name."""
        for agent in self.sub_agents:
            if agent.name == name:
                return agent
        return None

    def handle_alert(self, agent_name: str, message: str) -> None:
        """Handle alerts from sub-agents."""
        logger.warning(f"Alert from {agent_name}: {message}")
        # In the future, this could trigger notifications or automated fixes

