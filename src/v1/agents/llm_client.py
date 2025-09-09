

"""
LLM Client Wrapper
Provides a simple interface for agents to use LLM functionality with caching.
"""

from typing import Dict, Any, List, Optional, Tuple
from .llm_provider_manager import LLMProviderManager
from utils.llm_cache import llm_cache_decorator, global_llm_cache

# Global LLM provider manager instance
llm_manager = LLMProviderManager()

@llm_cache_decorator(ttl=3600, max_size=1000)
def chat_completion(
    messages: List[Dict[str, str]],
    model_name: Optional[str] = None,
    agent: Optional['BaseAgent'] = None,
    **kwargs
) -> str:
    """
    Generate chat completion using LLM with caching support.

    Args:
        messages: List of message dictionaries with 'role' and 'content'
        model_name: Optional model name to use (None for default)
        agent: Optional agent instance (if provided, uses agent's model if model_name is None)
        **kwargs: Additional parameters for the LLM call

    Returns:
        Generated text response
    """
    try:
        # Use agent's model if available and no model specified
        if agent and not model_name:
            model_name = agent.get_model_name()

        result = llm_manager.call_model(
            model_name=model_name,
            messages=messages,
            **kwargs
        )
        return result.get("response", "")
    except Exception as e:
        # Fallback to placeholder response if LLM call fails
        return f"LLM call failed: {str(e)}. Using fallback response."

@llm_cache_decorator(ttl=3600, max_size=1000)
def text_completion(
    prompt: str,
    model_name: Optional[str] = None,
    agent: Optional['BaseAgent'] = None,
    **kwargs
) -> str:
    """
    Generate text completion using LLM with caching support.

    Args:
        prompt: Input text prompt
        model_name: Optional model name to use (None for default)
        agent: Optional agent instance (if provided, uses agent's model if model_name is None)
        **kwargs: Additional parameters for the LLM call

    Returns:
        Generated text response
    """
    try:
        # Use agent's model if available and no model specified
        if agent and not model_name:
            model_name = agent.get_model_name()

        result = llm_manager.call_model(
            model_name=model_name,
            prompt=prompt,
            **kwargs
        )
        return result.get("response", "")
    except Exception as e:
        # Fallback to placeholder response if LLM call fails
        return f"LLM call failed: {str(e)}. Using fallback response."

def get_available_models() -> List[str]:
    """Get list of available LLM models."""
    return llm_manager.get_available_models()

def get_available_providers() -> List[str]:
    """Get list of available LLM providers."""
    from config.llm_config import get_available_providers
    return get_available_providers()

