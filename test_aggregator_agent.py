





"""
Test script for the AggregatorAgent.
"""

from agents import AggregatorAgent

def test_aggregator_agent():
    print("Testing AggregatorAgent...")

    # Create the agent
    aggregator = AggregatorAgent()

    # Test data
    document_text = """
    Настоящий договор аренды заключён между ООО "Ромашка" и ИП Иванов И.И.
    Сумма аренды: 50000 руб. в месяц. Срок: с 15.07.2023 по 15.07.2024.
    Контактный телефон: 8 (495) 123-45-67, email: contact@romashka.ru
    """

    structured_data = {
        "document_title": "Contract Agreement",
        "document_type": "contract",
        "date_created": "2024-01-01",
        "counterparty_name": "Company LLC",
        "signatory": "John Doe",
        "jurisdiction": "Russia"
    }

    print("1. Testing text processing...")
    result = aggregator.process("text", document_text)
    print(f"Cleaned text: {result['cleaned_text'][:100]}...")
    print(f"Agent name: {result['agent_name']}")
    print(f"Summary: {result['reflection_results']['summary']['summary']}")
    print(f"Sentiment analysis: {result['reflection_results']['sentiment_analysis']['sentiment_analysis']}")
    print(f"Ambiguity detected: {result['reflection_results']['ambiguity_detection']['ambiguity_detected']}")
    print()

    print("2. Testing document processing...")
    doc_result = aggregator.process_document(document_text, structured_data)
    print(f"Overall recommendation: {doc_result['overall_status']['recommendation']}")
    print(f"Issues found: {doc_result['overall_status']['issues_found']}")
    print()

    print("3. Testing status...")
    status = aggregator.get_status()
    print(f"Available agents: {list(status['available_agents'].keys())}")
    print()

if __name__ == "__main__":
    test_aggregator_agent()




