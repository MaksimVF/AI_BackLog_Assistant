









import os
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    COHERE = "cohere"
    GOOGLE = "google"
    LOCAL = "local"

class LLMModelConfig(BaseModel):
    """Configuration for a specific LLM model"""
    name: str
    provider: LLMProvider
    api_key: Optional[str] = None
    api_url: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 30
    is_default: bool = False

    @validator('temperature')
    def validate_temperature(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Temperature must be between 0 and 1')
        return v

class LLMConfig(BaseModel):
    """Configuration for LLM providers and models"""
    default_provider: LLMProvider = LLMProvider.OPENAI
    providers: Dict[LLMProvider, Dict[str, Any]] = Field(default_factory=dict)
    models: List[LLMModelConfig] = Field(default_factory=list)

    @property
    def default_model(self) -> Optional[LLMModelConfig]:
        """Get the default model configuration"""
        for model in self.models:
            if model.is_default:
                return model
        return self.models[0] if self.models else None

    def get_model_config(self, model_name: str) -> Optional[LLMModelConfig]:
        """Get configuration for a specific model"""
        for model in self.models:
            if model.name == model_name:
                return model
        return None

    def get_provider_config(self, provider: LLMProvider) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific provider"""
        return self.providers.get(provider)

def load_llm_config() -> LLMConfig:
    """Load LLM configuration from environment variables"""
    # Load from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
    cohere_api_key = os.getenv("COHERE_API_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")

    # Default models
    models = [
        LLMModelConfig(
            name="gpt-4",
            provider=LLMProvider.OPENAI,
            api_key=openai_api_key,
            max_tokens=8192,
            temperature=0.7,
            is_default=True
        ),
        LLMModelConfig(
            name="claude-2",
            provider=LLMProvider.ANTHROPIC,
            api_key=anthropic_api_key,
            max_tokens=100000,
            temperature=0.7
        ),
        LLMModelConfig(
            name="llama-2-7b",
            provider=LLMProvider.HUGGINGFACE,
            api_key=huggingface_api_key,
            max_tokens=4096,
            temperature=0.7
        )
    ]

    # Provider configurations
    providers = {
        LLMProvider.OPENAI: {
            "api_base": os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
            "organization": os.getenv("OPENAI_ORGANIZATION")
        },
        LLMProvider.ANTHROPIC: {
            "api_base": os.getenv("ANTHROPIC_API_BASE", "https://api.anthropic.com")
        },
        LLMProvider.HUGGINGFACE: {
            "api_base": os.getenv("HUGGINGFACE_API_BASE", "https://api-inference.huggingface.co")
        },
        LLMProvider.COHERE: {
            "api_base": os.getenv("COHERE_API_BASE", "https://api.cohere.ai")
        },
        LLMProvider.GOOGLE: {
            "api_base": os.getenv("GOOGLE_API_BASE", "https://generativelanguage.googleapis.com")
        },
        LLMProvider.LOCAL: {
            "api_base": os.getenv("LOCAL_API_BASE", "http://localhost:8080")
        }
    }

    # Determine default provider
    default_provider = LLMProvider.OPENAI
    if openai_api_key:
        default_provider = LLMProvider.OPENAI
    elif anthropic_api_key:
        default_provider = LLMProvider.ANTHROPIC
    elif huggingface_api_key:
        default_provider = LLMProvider.HUGGINGFACE

    return LLMConfig(
        default_provider=default_provider,
        providers=providers,
        models=models
    )

# Global LLM configuration
llm_config = load_llm_config()

def get_llm_config() -> LLMConfig:
    """Get the current LLM configuration"""
    return llm_config

def set_llm_config(config: LLMConfig):
    """Update the LLM configuration"""
    global llm_config
    llm_config = config

def add_model_config(model_config: LLMModelConfig):
    """Add a new model configuration"""
    global llm_config
    # Remove any existing model with same name
    llm_config.models = [m for m in llm_config.models if m.name != model_config.name]
    llm_config.models.append(model_config)

def remove_model_config(model_name: str):
    """Remove a model configuration"""
    global llm_config
    llm_config.models = [m for m in llm_config.models if m.name != model_name]

def set_default_model(model_name: str):
    """Set a model as default"""
    global llm_config
    # First reset all defaults
    for model in llm_config.models:
        model.is_default = False
    # Set the specified model as default
    for model in llm_config.models:
        if model.name == model_name:
            model.is_default = True
            break

def get_available_models() -> List[str]:
    """Get list of available model names"""
    return [model.name for model in llm_config.models]

def get_available_providers() -> List[str]:
    """Get list of available providers"""
    return [provider.value for provider in LLMProvider]

if __name__ == "__main__":
    # Example usage
    config = get_llm_config()
    print(f"Default provider: {config.default_provider}")
    print(f"Available models: {get_available_models()}")
    print(f"Default model: {config.default_model.name if config.default_model else 'None'}")

    # Add a custom model
    custom_model = LLMModelConfig(
        name="custom-model",
        provider=LLMProvider.LOCAL,
        api_url="http://localhost:5000/v1/models/custom",
        max_tokens=2048,
        temperature=0.5
    )
    add_model_config(custom_model)
    print(f"Updated models: {get_available_models()}")

    # Set default model
    set_default_model("custom-model")
    print(f"New default model: {config.default_model.name}")









