


from agents.analyzers.context_classifier import ContextClassifier
from unittest.mock import patch

def test_context_classifier_with_mock():
    classifier = ContextClassifier()

    # Mock the embedder to return fixed embeddings
    def mock_embed(text):
        # Simple mock: return different embeddings based on keywords
        if "банк" in text or "кредит" in text:
            return [0.1, 0.2, 0.3]  # Financial embedding
        elif "ужин" in text or "еда" in text:
            return [0.4, 0.5, 0.6]  # Household embedding
        else:
            return [0.7, 0.8, 0.9]  # General embedding

    # Test with mocked embeddings
    with patch('tools.semantic_embedder.SemanticEmbedder.embed', side_effect=mock_embed):
        history = [
            {
                "text": "У меня проблемы с кредитом",
                "context": "финансовый",
                "embedding": [0.1, 0.2, 0.3]  # Same as financial embedding
            },
            {
                "text": "Как приготовить ужин для семьи",
                "context": "бытовой",
                "embedding": [0.4, 0.5, 0.6]  # Same as household embedding
            }
        ]

        test_cases = [
            ("Мне нужна помощь с банковским счетом", "финансовый"),
            ("Как приготовить обед?", "бытовой"),
            ("Интересные факты о космосе", "общий"),
        ]

        print("Testing Context Classifier with Mock Embeddings...")
        for text, expected in test_cases:
            result = classifier.classify(text, history=history)
            print(f"Text: {text}")
            print(f"Expected: {expected}, Got: {result.context}")
            print(f"Confidence: {result.confidence:.2f}")
            print(f"Reasoning: {result.reasoning}")
            print("---")

if __name__ == "__main__":
    test_context_classifier_with_mock()


