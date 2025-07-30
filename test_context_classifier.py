

from agents.analyzers.context_classifier import ContextClassifier

def test_context_classifier():
    classifier = ContextClassifier()

    # Test cases
    test_cases = [
        ("Мне нужна помощь с моим стартапом, у нас проблемы с финансами", "профессиональный"),
        ("Чувствую себя очень плохо, у меня стресс на работе", "кризисный"),
        ("Как приготовить ужин для семьи?", "бытовой"),
        ("Какие налоги нужно платить за квартиру?", "финансовый"),
        ("Можно ли расторгнуть договор аренды?", "юридический"),
        ("Интересные факты о космосе", "общий"),
        ("Хочу заняться медитацией для улучшения настроения", "личный"),
    ]

    print("Testing Context Classifier...")
    for text, expected in test_cases:
        result = classifier.classify(text)
        print(f"Text: {text}")
        print(f"Expected: {expected}, Got: {result.context}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Reasoning: {result.reasoning}")
        print("---")

    # Test with history (semantic approach)
    print("\nTesting with history...")
    history = [
        {
            "text": "У меня проблемы с кредитом",
            "context": "финансовый",
            "embedding": [0.1, 0.2, 0.3]  # Mock embedding
        },
        {
            "text": "Как улучшить отношения с коллегами",
            "context": "профессиональный",
            "embedding": [0.4, 0.5, 0.6]  # Mock embedding
        }
    ]

    test_text = "Мне нужна помощь с банковским счетом"
    result = classifier.classify(test_text, history=history)
    print(f"Text: {test_text}")
    print(f"Result: {result.context}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reasoning: {result.reasoning}")

if __name__ == "__main__":
    test_context_classifier()

