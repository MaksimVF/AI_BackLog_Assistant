











"""
Fallback Planner

Provides fallback strategies when agents fail or timeout.
"""

from typing import Any, Dict, Optional

class FallbackPlanner:
    """
    Provides fallback strategies when agents fail or timeout.
    """

    def __init__(self, fallback_config: Optional[Dict[str, Any]] = None):
        """
        Initialize FallbackPlanner with fallback configuration.

        Args:
            fallback_config: Fallback configuration
        """
        self.fallback_config = fallback_config or {}

    def run(self, error_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines fallback strategy based on error context.

        Args:
            error_context: Error context information

        Returns:
            Fallback strategy
        """
        agent_name = error_context.get("agent")
        error_type = error_context.get("error_type")
        attempt = error_context.get("attempt", 1)

        strategy = self.fallback_config.get(agent_name, {}).get(error_type)

        if strategy:
            return {
                "agent": agent_name,
                "fallback": strategy,
                "attempt": attempt + 1,
                "action": "retry_with_fallback"
            }
        else:
            return {
                "agent": agent_name,
                "fallback": "manual_review",
                "attempt": attempt + 1,
                "action": "escalate"
            }












