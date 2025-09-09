



"""
Base Processor with Provider Selection Logic
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from src.common.config import settings

logger = logging.getLogger(__name__)

class BaseProcessor(ABC):
    """Base class for all modality processors with provider selection logic"""

    def __init__(self):
        self.available_providers = []
        self.current_provider = None

    @abstractmethod
    def _initialize_providers(self):
        """Initialize available providers"""
        pass

    @abstractmethod
    def _select_provider(self, input_data: Dict[str, Any]) -> str:
        """Select the best provider based on input characteristics"""
        pass

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input using the selected provider

        Args:
            input_data: Input data to process

        Returns:
            Processed data
        """
        # Initialize providers if not already done
        if not self.available_providers:
            self._initialize_providers()

        # Select the best provider for this input
        selected_provider = self._select_provider(input_data)

        try:
            # Process using the selected provider
            result = self._process_with_provider(selected_provider, input_data)
            logger.info(f"Processed with {selected_provider} provider")
            return result

        except Exception as e:
            logger.warning(f"Provider {selected_provider} failed: {e}. Trying fallback...")

            # Try fallback providers
            fallback_providers = [p for p in self.available_providers if p != selected_provider]

            for provider in fallback_providers:
                try:
                    result = self._process_with_provider(provider, input_data)
                    logger.info(f"Processed with fallback provider: {provider}")
                    return result
                except Exception as fallback_e:
                    logger.warning(f"Fallback provider {provider} also failed: {fallback_e}")
                    continue

            # If all providers fail, return error
            raise ValueError(f"All providers failed to process input: {e}")

    @abstractmethod
    def _process_with_provider(self, provider_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input using a specific provider"""
        pass

    def get_available_providers(self) -> list:
        """Get list of available providers"""
        return self.available_providers

