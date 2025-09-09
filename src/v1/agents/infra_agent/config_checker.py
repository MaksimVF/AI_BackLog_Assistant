




import os
from typing import Dict, Any, Optional, List
from .base_infra_agent import BaseInfraAgent

class ConfigCheckerAgent(BaseInfraAgent):
    """Agent to check and validate configuration."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        config = config or {}
        super().__init__(
            name="ConfigChecker",
            config={
                "required_env_vars": config.get("required_env_vars", [
                    "WEAVIATE_URL",
                    "REDIS_HOST",
                    "LLM_API_URL"
                ]),
                "optional_env_vars": config.get("optional_env_vars", [
                    "WEAVIATE_API_KEY",
                    "REDIS_PASSWORD",
                    "DEBUG_MODE"
                ])
            }
        )

    def check_status(self) -> Dict[str, Any]:
        """Check environment configuration."""
        missing_required = []
        present_optional = {}

        # Check required environment variables
        for var in self.config["required_env_vars"]:
            if var not in os.environ:
                missing_required.append(var)

        # Check optional environment variables
        for var in self.config["optional_env_vars"]:
            if var in os.environ:
                present_optional[var] = os.environ[var]

        # Determine status
        if missing_required:
            status = "incomplete"
        else:
            status = "complete"

        return {
            "status": status,
            "missing_required": missing_required,
            "present_optional": present_optional,
            "environment": {
                "required_count": len(self.config["required_env_vars"]),
                "optional_count": len(self.config["optional_env_vars"]),
                "present_count": len(self.config["required_env_vars"]) - len(missing_required) + len(present_optional)
            }
        }

    def validate_config(self, config_dict: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a configuration dictionary against a schema."""
        validation_errors = []

        for key, expected_type in schema.items():
            if key not in config_dict:
                validation_errors.append(f"Missing required key: {key}")
            elif not isinstance(config_dict[key], expected_type):
                validation_errors.append(f"Invalid type for {key}: expected {expected_type}, got {type(config_dict[key])}")

        if validation_errors:
            return {
                "status": "invalid",
                "errors": validation_errors
            }
        else:
            return {
                "status": "valid",
                "config": config_dict
            }

    def get_env_var(self, var_name: str, default: Any = None) -> Any:
        """Get an environment variable with a default value."""
        return os.environ.get(var_name, default)

    def list_all_env_vars(self, prefix: str = "") -> Dict[str, str]:
        """List all environment variables, optionally filtered by prefix."""
        env_vars = {}
        for key, value in os.environ.items():
            if prefix and key.startswith(prefix):
                env_vars[key] = value
            elif not prefix:
                env_vars[key] = value
        return env_vars




