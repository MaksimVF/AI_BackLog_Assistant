









import os
import logging
import requests
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from pydantic import BaseModel

# Import LLM configuration
from config.llm_config import (
    LLMConfig, LLMModelConfig, LLMProvider,
    get_llm_config, set_llm_config,
    add_model_config, remove_model_config,
    set_default_model, get_available_models
)

logger = logging.getLogger(__name__)

class LLMProviderError(Exception):
    """Custom exception for LLM provider errors"""
    pass

class LLMProviderManager:
    """Manager for LLM providers and models"""

    def __init__(self, config: Optional[LLMConfig] = None):
        """Initialize LLM provider manager"""
        self.config = config or get_llm_config()
        self._validate_config()

    def _validate_config(self):
        """Validate the LLM configuration"""
        if not self.config.models:
            raise LLMProviderError("No LLM models configured")

        if not self.config.default_model:
            logger.warning("No default model configured, using first available model")
            self.config.models[0].is_default = True

    def get_available_models(self) -> List[str]:
        """Get list of available model names"""
        return [model.name for model in self.config.models]

    def get_model_config(self, model_name: str) -> Optional[LLMModelConfig]:
        """Get configuration for a specific model"""
        return self.config.get_model_config(model_name)

    def set_default_model(self, model_name: str):
        """Set a model as default"""
        set_default_model(model_name)
        self.config = get_llm_config()  # Refresh config

    def add_model(self, model_config: LLMModelConfig):
        """Add a new model configuration"""
        add_model_config(model_config)
        self.config = get_llm_config()  # Refresh config

    def remove_model(self, model_name: str):
        """Remove a model configuration"""
        remove_model_config(model_name)
        self.config = get_llm_config()  # Refresh config

    def call_model(
        self,
        model_name: Optional[str] = None,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call an LLM model with the specified parameters

        Args:
            model_name: Name of the model to use (None for default)
            prompt: Simple prompt (for non-chat models)
            messages: List of messages (for chat models)
            max_tokens: Maximum tokens to generate
            temperature: Creativity temperature (0-1)
            **kwargs: Additional provider-specific parameters

        Returns:
            Dictionary with model response and metadata

        Raises:
            LLMProviderError: If the call fails
        """
        # Determine which model to use
        model_config = self._get_model_to_use(model_name)
        provider_config = self.config.get_provider_config(model_config.provider)

        # Prepare parameters
        params = self._prepare_call_parameters(
            model_config,
            provider_config,
            prompt,
            messages,
            max_tokens,
            temperature,
            **kwargs
        )

        try:
            # Call the appropriate provider
            if model_config.provider == LLMProvider.OPENAI:
                return self._call_openai(model_config, params)
            elif model_config.provider == LLMProvider.ANTHROPIC:
                return self._call_anthropic(model_config, params)
            elif model_config.provider == LLMProvider.HUGGINGFACE:
                return self._call_huggingface(model_config, params)
            elif model_config.provider == LLMProvider.COHERE:
                return self._call_cohere(model_config, params)
            elif model_config.provider == LLMProvider.GOOGLE:
                return self._call_google(model_config, params)
            elif model_config.provider == LLMProvider.LOCAL:
                return self._call_local(model_config, params)
            else:
                raise LLMProviderError(f"Unsupported provider: {model_config.provider}")

        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise LLMProviderError(f"Failed to call model {model_config.name}: {str(e)}")

    def _get_model_to_use(self, model_name: Optional[str]) -> LLMModelConfig:
        """Get the model configuration to use"""
        if model_name:
            model_config = self.config.get_model_config(model_name)
            if not model_config:
                raise LLMProviderError(f"Model not found: {model_name}")
            return model_config

        # Use default model
        if not self.config.default_model:
            raise LLMProviderError("No default model configured")
        return self.config.default_model

    def _prepare_call_parameters(
        self,
        model_config: LLMModelConfig,
        provider_config: Dict[str, Any],
        prompt: Optional[str],
        messages: Optional[List[Dict[str, str]]],
        max_tokens: Optional[int],
        temperature: Optional[float],
        **kwargs
    ) -> Dict[str, Any]:
        """Prepare parameters for LLM call"""
        params = {
            "model": model_config.name,
            "max_tokens": max_tokens or model_config.max_tokens,
            "temperature": temperature or model_config.temperature,
            **kwargs
        }

        # Add prompt or messages
        if prompt:
            params["prompt"] = prompt
        elif messages:
            params["messages"] = messages
        else:
            raise ValueError("Either prompt or messages must be provided")

        # Add API key if available
        if model_config.api_key:
            if model_config.provider == LLMProvider.OPENAI:
                params["api_key"] = model_config.api_key
            elif model_config.provider == LLMProvider.ANTHROPIC:
                params["api_key"] = model_config.api_key
            elif model_config.provider == LLMProvider.HUGGINGFACE:
                params["headers"] = {"Authorization": f"Bearer {model_config.api_key}"}
            elif model_config.provider == LLMProvider.COHERE:
                params["api_key"] = model_config.api_key
            elif model_config.provider == LLMProvider.GOOGLE:
                params["api_key"] = model_config.api_key

        # Add provider-specific configuration
        if provider_config:
            params.update(provider_config)

        return params

    def _call_openai(self, model_config: LLMModelConfig, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call OpenAI API"""
        api_base = params.pop("api_base", "https://api.openai.com/v1")
        api_key = params.pop("api_key", model_config.api_key)

        if not api_key:
            raise LLMProviderError("OpenAI API key not configured")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Determine endpoint
        endpoint = "chat/completions" if "messages" in params else "completions"
        url = f"{api_base}/v1/{endpoint}"

        # Prepare payload
        payload = {
            "model": model_config.name,
            "max_tokens": params.get("max_tokens", model_config.max_tokens),
            "temperature": params.get("temperature", model_config.temperature)
        }

        if "messages" in params:
            payload["messages"] = params["messages"]
        else:
            payload["prompt"] = params.get("prompt", "")

        # Add additional parameters
        for key, value in params.items():
            if key not in ["api_base", "api_key", "model", "max_tokens", "temperature", "prompt", "messages"]:
                payload[key] = value

        # Make request
        response = requests.post(url, json=payload, headers=headers, timeout=model_config.timeout)
        response.raise_for_status()

        result = response.json()

        # Process result
        if "choices" in result and len(result["choices"]) > 0:
            return {
                "response": result["choices"][0]["message"]["content"] if "messages" in params else result["choices"][0]["text"],
                "usage": result.get("usage", {}),
                "model": model_config.name,
                "provider": model_config.provider.value
            }
        else:
            raise LLMProviderError(f"Invalid response format: {result}")

    def _call_anthropic(self, model_config: LLMModelConfig, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Anthropic API"""
        api_base = params.pop("api_base", "https://api.anthropic.com")
        api_key = params.pop("api_key", model_config.api_key)

        if not api_key:
            raise LLMProviderError("Anthropic API key not configured")

        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        url = f"{api_base}/v1/complete"

        # Prepare payload
        payload = {
            "model": model_config.name,
            "max_tokens_to_sample": params.get("max_tokens", model_config.max_tokens),
            "temperature": params.get("temperature", model_config.temperature),
            "prompt": params.get("prompt", "")
        }

        # Add additional parameters
        for key, value in params.items():
            if key not in ["api_base", "api_key", "model", "max_tokens_to_sample", "temperature", "prompt"]:
                payload[key] = value

        # Make request
        response = requests.post(url, json=payload, headers=headers, timeout=model_config.timeout)
        response.raise_for_status()

        result = response.json()

        # Process result
        if "completion" in result:
            return {
                "response": result["completion"],
                "usage": {
                    "input_tokens": result.get("input_tokens", 0),
                    "output_tokens": result.get("output_tokens", 0)
                },
                "model": model_config.name,
                "provider": model_config.provider.value
            }
        else:
            raise LLMProviderError(f"Invalid response format: {result}")

    def _call_huggingface(self, model_config: LLMModelConfig, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Hugging Face API"""
        api_base = params.pop("api_base", "https://api-inference.huggingface.co")
        api_key = model_config.api_key

        if not api_key:
            raise LLMProviderError("Hugging Face API key not configured")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        url = f"{api_base}/models/{model_config.name}"

        # Prepare payload
        payload = {
            "inputs": params.get("prompt", ""),
            "parameters": {
                "max_new_tokens": params.get("max_tokens", model_config.max_tokens),
                "temperature": params.get("temperature", model_config.temperature)
            }
        }

        # Add additional parameters
        for key, value in params.items():
            if key not in ["api_base", "api_key", "model", "max_tokens", "temperature", "prompt"]:
                payload["parameters"][key] = value

        # Make request
        response = requests.post(url, json=payload, headers=headers, timeout=model_config.timeout)
        response.raise_for_status()

        result = response.json()

        # Process result
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            return {
                "response": result[0]["generated_text"],
                "usage": {
                    "input_tokens": len(params.get("prompt", "").split()),
                    "output_tokens": len(result[0]["generated_text"].split())
                },
                "model": model_config.name,
                "provider": model_config.provider.value
            }
        else:
            raise LLMProviderError(f"Invalid response format: {result}")

    def _call_cohere(self, model_config: LLMModelConfig, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Cohere API"""
        api_base = params.pop("api_base", "https://api.cohere.ai")
        api_key = params.pop("api_key", model_config.api_key)

        if not api_key:
            raise LLMProviderError("Cohere API key not configured")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        url = f"{api_base}/v1/generate"

        # Prepare payload
        payload = {
            "model": model_config.name,
            "max_tokens": params.get("max_tokens", model_config.max_tokens),
            "temperature": params.get("temperature", model_config.temperature),
            "prompt": params.get("prompt", "")
        }

        # Add additional parameters
        for key, value in params.items():
            if key not in ["api_base", "api_key", "model", "max_tokens", "temperature", "prompt"]:
                payload[key] = value

        # Make request
        response = requests.post(url, json=payload, headers=headers, timeout=model_config.timeout)
        response.raise_for_status()

        result = response.json()

        # Process result
        if "generations" in result and len(result["generations"]) > 0:
            return {
                "response": result["generations"][0]["text"],
                "usage": {
                    "input_tokens": result.get("meta", {}).get("tokens", {}).get("input_tokens", 0),
                    "output_tokens": result.get("meta", {}).get("tokens", {}).get("output_tokens", 0)
                },
                "model": model_config.name,
                "provider": model_config.provider.value
            }
        else:
            raise LLMProviderError(f"Invalid response format: {result}")

    def _call_google(self, model_config: LLMModelConfig, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Google Generative Language API"""
        api_base = params.pop("api_base", "https://generativelanguage.googleapis.com")
        api_key = params.pop("api_key", model_config.api_key)

        if not api_key:
            raise LLMProviderError("Google API key not configured")

        url = f"{api_base}/v1beta/models/{model_config.name}:generateContent?key={api_key}"

        # Prepare payload
        if "messages" in params:
            # Convert messages to Google format
            contents = []
            for message in params["messages"]:
                contents.append({
                    "role": message.get("role", "user"),
                    "parts": [{"text": message["content"]}]
                })
            payload = {"contents": contents}
        else:
            payload = {
                "contents": [{
                    "role": "user",
                    "parts": [{"text": params.get("prompt", "")}]
                }]
            }

        # Add generation config
        payload["generationConfig"] = {
            "maxOutputTokens": params.get("max_tokens", model_config.max_tokens),
            "temperature": params.get("temperature", model_config.temperature)
        }

        # Add additional parameters
        for key, value in params.items():
            if key not in ["api_base", "api_key", "model", "max_tokens", "temperature", "prompt", "messages"]:
                payload[key] = value

        # Make request
        response = requests.post(url, json=payload, timeout=model_config.timeout)
        response.raise_for_status()

        result = response.json()

        # Process result
        if "candidates" in result and len(result["candidates"]) > 0:
            return {
                "response": result["candidates"][0]["content"]["parts"][0]["text"],
                "usage": {
                    "input_tokens": result.get("usageMetadata", {}).get("inputTokenCount", 0),
                    "output_tokens": result.get("usageMetadata", {}).get("outputTokenCount", 0)
                },
                "model": model_config.name,
                "provider": model_config.provider.value
            }
        else:
            raise LLMProviderError(f"Invalid response format: {result}")

    def _call_local(self, model_config: LLMModelConfig, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call local LLM API"""
        api_base = params.pop("api_base", "http://localhost:8080")
        api_key = model_config.api_key

        url = f"{api_base}/v1/complete"

        # Prepare payload
        payload = {
            "model": model_config.name,
            "max_tokens": params.get("max_tokens", model_config.max_tokens),
            "temperature": params.get("temperature", model_config.temperature),
            "prompt": params.get("prompt", "")
        }

        # Add additional parameters
        for key, value in params.items():
            if key not in ["api_base", "api_key", "model", "max_tokens", "temperature", "prompt"]:
                payload[key] = value

        # Add API key if available
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        # Make request
        response = requests.post(url, json=payload, headers=headers, timeout=model_config.timeout)
        response.raise_for_status()

        result = response.json()

        # Process result
        if "response" in result:
            return {
                "response": result["response"],
                "usage": {
                    "input_tokens": result.get("input_tokens", 0),
                    "output_tokens": result.get("output_tokens", 0)
                },
                "model": model_config.name,
                "provider": model_config.provider.value
            }
        else:
            raise LLMProviderError(f"Invalid response format: {result}")

    def get_provider_status(self, provider: LLMProvider) -> Dict[str, Any]:
        """Get status of a specific provider"""
        try:
            provider_config = self.config.get_provider_config(provider)
            if not provider_config:
                return {"status": "error", "message": "Provider not configured"}

            # Check connectivity
            if provider == LLMProvider.OPENAI:
                return self._check_openai_status(provider_config)
            elif provider == LLMProvider.ANTHROPIC:
                return self._check_anthropic_status(provider_config)
            elif provider == LLMProvider.HUGGINGFACE:
                return self._check_huggingface_status(provider_config)
            elif provider == LLMProvider.COHERE:
                return self._check_cohere_status(provider_config)
            elif provider == LLMProvider.GOOGLE:
                return self._check_google_status(provider_config)
            elif provider == LLMProvider.LOCAL:
                return self._check_local_status(provider_config)
            else:
                return {"status": "error", "message": "Unsupported provider"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _check_openai_status(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check OpenAI provider status"""
        api_key = provider_config.get("api_key") or self.config.default_model.api_key if self.config.default_model else None

        if not api_key:
            return {"status": "error", "message": "API key not configured"}

        try:
            # Test API connectivity
            url = f"{provider_config.get('api_base', 'https://api.openai.com/v1')}/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()

            result = response.json()
            return {
                "status": "ok",
                "message": "OpenAI API is accessible",
                "models_available": len(result.get("data", []))
            }
        except Exception as e:
            return {"status": "error", "message": f"OpenAI API check failed: {str(e)}"}

    def _check_anthropic_status(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check Anthropic provider status"""
        api_key = provider_config.get("api_key") or self.config.default_model.api_key if self.config.default_model else None

        if not api_key:
            return {"status": "error", "message": "API key not configured"}

        try:
            # Test API connectivity
            url = f"{provider_config.get('api_base', 'https://api.anthropic.com')}/v1/health"
            headers = {"x-api-key": api_key}
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()

            return {
                "status": "ok",
                "message": "Anthropic API is accessible"
            }
        except Exception as e:
            return {"status": "error", "message": f"Anthropic API check failed: {str(e)}"}

    def _check_huggingface_status(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check Hugging Face provider status"""
        api_key = provider_config.get("api_key") or self.config.default_model.api_key if self.config.default_model else None

        if not api_key:
            return {"status": "error", "message": "API key not configured"}

        try:
            # Test API connectivity
            url = f"{provider_config.get('api_base', 'https://api-inference.huggingface.co')}/status"
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()

            return {
                "status": "ok",
                "message": "Hugging Face API is accessible"
            }
        except Exception as e:
            return {"status": "error", "message": f"Hugging Face API check failed: {str(e)}"}

    def _check_cohere_status(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check Cohere provider status"""
        api_key = provider_config.get("api_key") or self.config.default_model.api_key if self.config.default_model else None

        if not api_key:
            return {"status": "error", "message": "API key not configured"}

        try:
            # Test API connectivity
            url = f"{provider_config.get('api_base', 'https://api.cohere.ai')}/v1/health"
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()

            return {
                "status": "ok",
                "message": "Cohere API is accessible"
            }
        except Exception as e:
            return {"status": "error", "message": f"Cohere API check failed: {str(e)}"}

    def _check_google_status(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check Google provider status"""
        api_key = provider_config.get("api_key") or self.config.default_model.api_key if self.config.default_model else None

        if not api_key:
            return {"status": "error", "message": "API key not configured"}

        try:
            # Test API connectivity
            url = f"{provider_config.get('api_base', 'https://generativelanguage.googleapis.com')}/v1beta/models"
            params = {"key": api_key}
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            result = response.json()
            return {
                "status": "ok",
                "message": "Google API is accessible",
                "models_available": len(result.get("models", []))
            }
        except Exception as e:
            return {"status": "error", "message": f"Google API check failed: {str(e)}"}

    def _check_local_status(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check local provider status"""
        try:
            # Test API connectivity
            url = f"{provider_config.get('api_base', 'http://localhost:8080')}/health"
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            return {
                "status": "ok",
                "message": "Local API is accessible"
            }
        except Exception as e:
            return {"status": "error", "message": f"Local API check failed: {str(e)}"}

    def update_provider_config(self, provider: LLMProvider, config: Dict[str, Any]):
        """Update configuration for a specific provider"""
        self.config.providers[provider] = config
        set_llm_config(self.config)

    def update_model_config(self, model_name: str, config: Dict[str, Any]):
        """Update configuration for a specific model"""
        model = self.config.get_model_config(model_name)
        if not model:
            raise LLMProviderError(f"Model not found: {model_name}")

        # Update model configuration
        for key, value in config.items():
            if hasattr(model, key):
                setattr(model, key, value)

        set_llm_config(self.config)

    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get usage statistics for LLM calls"""
        # This would be implemented with actual tracking
        return {
            "total_calls": 0,
            "calls_by_provider": {},
            "calls_by_model": {},
            "token_usage": {
                "input_tokens": 0,
                "output_tokens": 0
            }
        }

# Example usage
if __name__ == "__main__":
    # Initialize provider manager
    manager = LLMProviderManager()

    # Test model call
    try:
        result = manager.call_model(
            model_name="gpt-4",
            prompt="Hello, how are you?",
            max_tokens=50,
            temperature=0.7
        )
        print(f"Model response: {result['response']}")
        print(f"Usage: {result['usage']}")
    except LLMProviderError as e:
        print(f"Error: {e}")

    # Test provider status
    status = manager.get_provider_status(LLMProvider.OPENAI)
    print(f"OpenAI status: {status}")

    # List available models
    print(f"Available models: {manager.get_available_models()}")









