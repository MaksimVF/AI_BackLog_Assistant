

"""
OpenAI LLM client implementation.
"""

import os
from typing import Dict, Any, List, Optional
import openai
from .llm_base_client import LLMClient

class OpenAIClient(LLMClient):
    """OpenAI LLM client implementation."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize OpenAI client with API key and configuration."""
        self.config = config
        self.api_key = config.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.model = config.get("model", "gpt-4o-mini")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 1000)

        if not self.api_key:
            raise ValueError("OpenAI API key not provided in config or environment")

        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)

    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate chat completion using OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].message.content

    def text_completion(self, prompt: str, **kwargs) -> str:
        """Generate text completion using OpenAI API."""
        response = self.client.completions.create(
            model=self.model,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].text

    def embeddings(self, text: str) -> List[float]:
        """Generate embeddings using OpenAI API."""
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "openai"

    @property
    def model_name(self) -> str:
        """Return model name."""
        return self.model

