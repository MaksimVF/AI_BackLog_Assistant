


from agents.analyzers.intent_identifier import IntentIdentifier
from unittest.mock import patch

def test_intent_identifier():
    identifier = IntentIdentifier()

    # Test cases for keyword matching
    test_cases = [
        ("Как работает эта система?", "вопрос"),
        ("Мне нужно сделать отчет к завтра", "задача"),
        ("Я заметил интересный факт о данных", "наблюдение"),
        ("Со мной случилось что-то странное", "опыт"),
        ("Поэтому я думаю, что это правильное решение", "вывод"),
        ("Что если мы попробуем другой подход?", "размышление"),
        ("Помогите! У нас кризис!", "кризис"),
        ("Просто текст без явного намерения", "неизвестно"),
    ]

    print("Testing Intent Identifier (keyword matching)...")
    for text, expected in test_cases:
        result = identifier.identify(text)
        print(f"Text: {text}")
        print(f"Expected: {expected}, Got: {result.intent_type}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Reasoning: {result.reasoning}")
        print("---")

    # Test with mocked LLM
    print("\nTesting Intent Identifier with Mock LLM...")

    def mock_llm_call(prompt):
        # Simple mock: return intent based on keywords in the text
        if "кризис" in prompt or "помогите" in prompt:
            return "кризис"
        elif "что если" in prompt or "возможно" in prompt:
            return "размышление"
        elif "как" in prompt or "что" in prompt:
            return "вопрос"
        else:
            return "неизвестно"

    with patch('tools.llm_tool.LLMTool.call_intent_model', side_effect=mock_llm_call):
        # Test case that would trigger LLM (low confidence from keywords)
        text = "Что если мы попробуем использовать другой алгоритм?"
        result = identifier.identify(text)
        print(f"Text: {text}")
        print(f"Result: {result.intent_type}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Reasoning: {result.reasoning}")

if __name__ == "__main__":
    test_intent_identifier()


