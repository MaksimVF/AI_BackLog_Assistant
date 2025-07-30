



import requests
from typing import Dict, Any, Optional, List
from .base_infra_agent import BaseInfraAgent

class LLMCheckerAgent(BaseInfraAgent):
    """Agent to check LLM model availability and health."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        config = config or {}
        super().__init__(
            name="LLMChecker",
            config={
                "models": config.get("models", [
                    {
                        "name": "local_llm",
                        "url": "http://localhost:5000/generate",
                        "type": "text_generation",
                        "timeout": 10
                    }
                ])
            }
        )

    def check_status(self) -> Dict[str, Any]:
        """Check all configured LLM models."""
        model_statuses = {}

        for model_config in self.config["models"]:
            model_name = model_config["name"]
            model_type = model_config.get("type", "unknown")

            try:
                if model_type == "text_generation":
                    status = self._check_text_generation_model(model_config)
                else:
                    status = self._check_generic_model(model_config)

                model_statuses[model_name] = status
            except Exception as e:
                model_statuses[model_name] = {
                    "status": "error",
                    "error": str(e),
                    "type": model_type
                }

        # Determine overall status
        all_statuses = [status.get("status", "error") for status in model_statuses.values()]
        overall_status = "degraded" if "error" in all_statuses else "healthy"

        return {
            "status": overall_status,
            "models": model_statuses
        }

    def _check_text_generation_model(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check a text generation model."""
        url = model_config["url"]
        timeout = model_config.get("timeout", 10)

        try:
            # Send a simple test prompt
            test_prompt = "Test"
            response = requests.post(
                url,
                json={"prompt": test_prompt, "max_tokens": 5},
                timeout=timeout
            )
            response.raise_for_status()

            # Check if we got a valid response
            result = response.json()
            if "generated_text" in result or "choices" in result:
                return {
                    "status": "healthy",
                    "response_time": response.elapsed.total_seconds(),
                    "test_output": result.get("generated_text", "OK")[:50]
                }
            else:
                return {
                    "status": "unexpected_response",
                    "details": result
                }
        except requests.RequestException as e:
            return {
                "status": "unavailable",
                "error": str(e)
            }

    def _check_generic_model(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check a generic model with a simple ping."""
        url = model_config["url"]
        timeout = model_config.get("timeout", 5)

        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return {
                "status": "healthy",
                "response_time": response.elapsed.total_seconds()
            }
        except requests.RequestException as e:
            return {
                "status": "unavailable",
                "error": str(e)
            }

    def test_model(self, model_name: str, test_input: str) -> Dict[str, Any]:
        """Test a specific model with custom input."""
        for model_config in self.config["models"]:
            if model_config["name"] == model_name:
                try:
                    if model_config.get("type") == "text_generation":
                        return self._test_text_generation(model_config, test_input)
                    else:
                        return {"status": "unsupported", "model": model_name}
                except Exception as e:
                    return {"status": "error", "error": str(e), "model": model_name}

        return {"status": "not_found", "model": model_name}

    def _test_text_generation(self, model_config: Dict[str, Any], test_input: str) -> Dict[str, Any]:
        """Test text generation with custom input."""
        url = model_config["url"]
        timeout = model_config.get("timeout", 10)

        try:
            response = requests.post(
                url,
                json={"prompt": test_input, "max_tokens": 20},
                timeout=timeout
            )
            response.raise_for_status()

            result = response.json()
            return {
                "status": "success",
                "input": test_input,
                "output": result.get("generated_text", "No output")[:100]
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "input": test_input,
                "error": str(e)
            }




