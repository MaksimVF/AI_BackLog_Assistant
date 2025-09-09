
"""
Abstract base class for LLM clients.
All LLM providers should implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def __init__(self, config: Dict[str, Any]):
        """Initialize the LLM client with configuration."""
        pass

    @abstractmethod
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate chat completion.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text response
        """
        pass

    @abstractmethod
    def text_completion(self, prompt: str, **kwargs) -> str:
        """
        Generate text completion from a prompt.

        Args:
            prompt: Input text prompt
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text response
        """
        pass

    @abstractmethod
    def embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings for text.

        Args:
            text: Input text

        Returns:
            List of embedding floats
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of the LLM provider."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the name of the model being used."""
        pass
