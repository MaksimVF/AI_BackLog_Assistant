


import requests
from typing import Dict, Any, Optional
from .base_infra_agent import BaseInfraAgent

class WeaviateCheckerAgent(BaseInfraAgent):
    """Agent to check Weaviate connection and status."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        config = config or {}
        super().__init__(
            name="WeaviateChecker",
            config={
                "url": config.get("url", "http://localhost:8081"),
                "api_key": config.get("api_key"),
                "timeout": config.get("timeout", 5)
            }
        )

    def check_status(self) -> Dict[str, Any]:
        """Check Weaviate connection and status."""
        url = f"{self.config['url']}/v1/.well-known/ready"

        try:
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {self.config['api_key']}"} if self.config.get("api_key") else {},
                timeout=self.config["timeout"]
            )
            response.raise_for_status()

            # Check if Weaviate is ready
            if response.json().get("status") == "green":
                return {
                    "status": "healthy",
                    "url": self.config["url"],
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "status": "degraded",
                    "url": self.config["url"],
                    "details": response.json()
                }
        except requests.RequestException as e:
            return {
                "status": "unavailable",
                "url": self.config["url"],
                "error": str(e)
            }

    def test_query(self, query: str = "test") -> Dict[str, Any]:
        """Test a simple query to Weaviate."""
        url = f"{self.config['url']}/v1/graphql"
        graphql_query = {
            "query": f"""
            {{
              Get {{
                DocumentChunk(limit: 1) {{
                  text
                }}
              }}
            }}
            """
        }

        try:
            response = requests.post(
                url,
                json=graphql_query,
                headers={"Authorization": f"Bearer {self.config['api_key']}"} if self.config.get("api_key") else {},
                timeout=self.config["timeout"]
            )
            response.raise_for_status()
            return {
                "status": "success",
                "result": response.json()
            }
        except requests.RequestException as e:
            return {
                "status": "failed",
                "error": str(e)
            }


