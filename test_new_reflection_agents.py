



"""
Test script for the new reflection agents.
"""

from agents.reflection import (
    FactVerificationAgent,
    AdvancedSentimentAndToneAnalyzer,
    SummaryGenerator
)

def test_fact_verification_agent():
    print("Testing FactVerificationAgent...")
    agent = FactVerificationAgent()

    # Mock text for testing
    test_text = """
    Москва — столица России. Население Москвы составляет около 15 миллионов человек.
    Эйфелева башня находится в Париже и была построена в 1889 году.
    """

    # Note: This will actually call the LLM, so we should mock it in a real test
    # For now, we'll just show the structure
    try:
        result = agent.verify_facts(test_text)
        print(f"Verification results: {result['verification_results']}")
    except Exception as e:
        print(f"Fact verification would call LLM with prompt containing: {test_text[:50]}...")
        print(f"Mock result structure: {{'verification_results': ['Факты подтверждаются.', ...]}}")
    print()

def test_advanced_sentiment_tone_analyzer():
    print("Testing AdvancedSentimentAndToneAnalyzer...")
    analyzer = AdvancedSentimentAndToneAnalyzer()

    # Mock text for testing
    test_text = """
    Уважаемые коллеги, мы рады сообщить о значительном прогрессе в нашем проекте.
    Команда проделала отличную работу, и мы уверены в успешном завершении.
    """

    # Note: This will actually call the LLM, so we should mock it in a real test
    try:
        result = analyzer.analyze(test_text)
        print(f"Sentiment analysis: {result['sentiment_analysis']}")
    except Exception as e:
        print(f"Advanced sentiment analysis would call LLM with prompt containing: {test_text[:50]}...")
        print(f"Mock result structure: {{'sentiment_analysis': 'Эмоциональная тональность: позитивная, Стиль: формальный, ...'}}")
    print()

def test_summary_generator():
    print("Testing SummaryGenerator...")
    generator = SummaryGenerator()

    # Mock text for testing
    test_text = """
    В соответствии с настоящим договором, стороны обязуются выполнить работы
    в установленные сроки и согласно утвержденному плану. Договор вступает в силу
    с момента подписания и действует до 31 декабря 2025 года.
    """

    # Note: This will actually call the LLM, so we should mock it in a real test
    try:
        result = generator.generate_summary(test_text)
        print(f"Summary: {result['summary']}")
    except Exception as e:
        print(f"Summary generation would call LLM with prompt containing: {test_text[:50]}...")
        print(f"Mock result structure: {{'summary': 'Стороны обязуются выполнить работы по договору до 2025 года.'}}")
    print()

if __name__ == "__main__":
    print("Note: These tests would normally call LLM APIs. In production, you would:")
    print("1. Set up proper API keys and endpoints")
    print("2. Mock the LLM responses for testing")
    print("3. Handle rate limits and errors appropriately")
    print()

    test_fact_verification_agent()
    test_advanced_sentiment_tone_analyzer()
    test_summary_generator()


