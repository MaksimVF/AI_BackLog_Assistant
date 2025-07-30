

import requests
from typing import Optional, Dict, Any

class LLMTool:
    """Interface for calling LLM models"""

    def __init__(self, api_url: str = "http://localhost:8080/complete"):
        """
        Initialize LLM tool with API endpoint

        Args:
            api_url: URL of the LLM API endpoint
        """
        self.api_url = api_url

    def call_model(self, prompt: str, max_tokens: int = 50, temperature: float = 0.7) -> Optional[str]:
        """
        Call LLM model with a prompt

        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens to generate
            temperature: Creativity temperature (0-1)

        Returns:
            Model response or None if failed
        """
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except requests.RequestException as e:
            print(f"[ERROR] LLM call failed: {e}")
            return None

    def call_intent_model(self, prompt: str) -> Optional[str]:
        """
        Call LLM model specifically for intent classification

        Args:
            prompt: Intent classification prompt

        Returns:
            Intent classification result
        """
        return self.call_model(prompt, max_tokens=10, temperature=0.3)

