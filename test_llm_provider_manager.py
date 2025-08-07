









import os
import unittest
from unittest.mock import patch, MagicMock
from agents.llm_provider_manager import LLMProviderManager, LLMProvider, LLMProviderError
from config.llm_config import LLMModelConfig, LLMProvider

class TestLLMProviderManager(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        # Mock environment variables for API keys
        os.environ["OPENAI_API_KEY"] = "test_openai_key"
        os.environ["ANTHROPIC_API_KEY"] = "test_anthropic_key"
        os.environ["HUGGINGFACE_API_KEY"] = "test_huggingface_key"

        # Initialize manager
        self.manager = LLMProviderManager()

    def test_initialization(self):
        """Test manager initialization"""
        self.assertIsNotNone(self.manager)
        self.assertIsNotNone(self.manager.config)
        self.assertGreater(len(self.manager.config.models), 0)

    def test_get_available_models(self):
        """Test getting available models"""
        models = self.manager.get_available_models()
        self.assertIsInstance(models, list)
        self.assertGreater(len(models), 0)
        self.assertIn("gpt-4", models)

    def test_set_default_model(self):
        """Test setting default model"""
        # Add a test model first
        test_model = LLMModelConfig(
            name="test-model",
            provider=LLMProvider.LOCAL,
            api_url="http://localhost:5000",
            is_default=False
        )
        self.manager.add_model(test_model)

        # Set as default
        self.manager.set_default_model("test-model")

        # Verify
        default_model = self.manager.config.default_model
        self.assertIsNotNone(default_model)
        self.assertEqual(default_model.name, "test-model")

    def test_add_remove_model(self):
        """Test adding and removing models"""
        # Add a test model
        test_model = LLMModelConfig(
            name="test-model",
            provider=LLMProvider.LOCAL,
            api_url="http://localhost:5000",
            is_default=False
        )
        self.manager.add_model(test_model)

        # Verify addition
        models = self.manager.get_available_models()
        self.assertIn("test-model", models)

        # Remove model
        self.manager.remove_model("test-model")

        # Verify removal
        models = self.manager.get_available_models()
        self.assertNotIn("test-model", models)

    @patch('requests.post')
    def test_call_model_success(self, mock_post):
        """Test successful model call"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"text": "Hello, I'm fine!"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Call model
        result = self.manager.call_model(
            model_name="gpt-4",
            prompt="Hello, how are you?",
            max_tokens=50
        )

        # Verify result
        self.assertIn("response", result)
        self.assertEqual(result["response"], "Hello, I'm fine!")
        self.assertIn("usage", result)

    @patch('requests.post')
    def test_call_model_failure(self, mock_post):
        """Test failed model call"""
        # Mock failed response
        mock_post.side_effect = Exception("API failure")

        # Test error handling
        with self.assertRaises(LLMProviderError):
            self.manager.call_model(
                model_name="gpt-4",
                prompt="Hello, how are you?",
                max_tokens=50
            )

    @patch('requests.get')
    def test_provider_status_check(self, mock_get):
        """Test provider status check"""
        # Mock successful status response
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"id": "gpt-4"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Check status
        status = self.manager.get_provider_status(LLMProvider.OPENAI)

        # Verify status
        self.assertEqual(status["status"], "ok")
        self.assertIn("models_available", status)

    def test_update_provider_config(self):
        """Test updating provider configuration"""
        # Update provider config
        new_config = {
            "api_base": "https://custom-api.openai.com",
            "organization": "test-org"
        }
        self.manager.update_provider_config(LLMProvider.OPENAI, new_config)

        # Verify update
        provider_config = self.manager.config.get_provider_config(LLMProvider.OPENAI)
        self.assertEqual(provider_config["api_base"], "https://custom-api.openai.com")
        self.assertEqual(provider_config["organization"], "test-org")

    def test_update_model_config(self):
        """Test updating model configuration"""
        # Update model config
        updates = {
            "max_tokens": 2048,
            "temperature": 0.5
        }
        self.manager.update_model_config("gpt-4", updates)

        # Verify update
        model_config = self.manager.config.get_model_config("gpt-4")
        self.assertEqual(model_config.max_tokens, 2048)
        self.assertEqual(model_config.temperature, 0.5)

    def test_invalid_model_selection(self):
        """Test error handling for invalid model"""
        with self.assertRaises(LLMProviderError):
            self.manager.call_model(
                model_name="nonexistent-model",
                prompt="Test",
                max_tokens=50
            )

    def test_missing_api_key(self):
        """Test error handling for missing API key"""
        # Remove API key from environment
        os.environ["OPENAI_API_KEY"] = ""

        # Reinitialize manager
        manager = LLMProviderManager()

        # Test with model that requires API key
        with self.assertRaises(LLMProviderError):
            manager.call_model(
                model_name="gpt-4",
                prompt="Test",
                max_tokens=50
            )

if __name__ == "__main__":
    unittest.main()











