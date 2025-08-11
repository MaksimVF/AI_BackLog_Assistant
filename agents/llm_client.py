

"""
LLM Client Wrapper
Provides a simple interface for agents to use LLM functionality.
"""

from typing import Dict, Any, List, Optional
from .llm_provider_manager import LLMProviderManager

# Global LLM provider manager instance
llm_manager = LLMProviderManager()

def chat_completion(
    messages: List[Dict[str, str]],
    model_name: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate chat completion using LLM.

    Args:
        messages: List of message dictionaries with 'role' and 'content'
        model_name: Optional model name to use (None for default)
        **kwargs: Additional parameters for the LLM call

    Returns:
        Generated text response
    """
    try:
        result = llm_manager.call_model(
            model_name=model_name,
            messages=messages,
            **kwargs
        )
        return result.get("response", "")
    except Exception as e:
        # Fallback to placeholder response if LLM call fails
        return f"LLM call failed: {str(e)}. Using fallback response."

def text_completion(
    prompt: str,
    model_name: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate text completion using LLM.

    Args:
        prompt: Input text prompt
        model_name: Optional model name to use (None for default)
        **kwargs: Additional parameters for the LLM call

    Returns:
        Generated text response
    """
    try:
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

