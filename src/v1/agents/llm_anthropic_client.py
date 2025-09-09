


"""
Anthropic LLM client implementation.
"""

import os
from typing import Dict, Any, List, Optional
import anthropic
from .llm_base_client import LLMClient

class AnthropicClient(LLMClient):
    """Anthropic LLM client implementation."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize Anthropic client with API key and configuration."""
        self.config = config
        self.api_key = config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        self.model = config.get("model", "claude-3-haiku-20240307")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 1000)

        if not self.api_key:
            raise ValueError("Anthropic API key not provided in config or environment")

        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate chat completion using Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.content[0].text

    def text_completion(self, prompt: str, **kwargs) -> str:
        """Generate text completion using Anthropic API."""
        response = self.client.completions.create(
            model=self.model,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.completion

    def embeddings(self, text: str) -> List[float]:
        """Generate embeddings using Anthropic API (if available)."""
        # Note: Anthropic's embedding API might be different
        # This is a placeholder implementation
        raise NotImplementedError("Anthropic embeddings not yet implemented")

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "anthropic"

    @property
    def model_name(self) -> str:
        """Return model name."""
        return self.model


