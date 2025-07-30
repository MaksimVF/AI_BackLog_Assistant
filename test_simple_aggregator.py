





"""
Simple test script for the AggregatorAgent without external dependencies.
"""

def test_aggregator_agent():
    print("Testing AggregatorAgent (simplified)...")

    # Import here to avoid dependency issues
    from agents.aggregator_agent import AggregatorAgent

    # Create the agent
    aggregator = AggregatorAgent()

    # Test data
    document_text = """
    Настоящий договор аренды заключён между ООО "Ромашка" и ИП Иванов И.И.
    Сумма аренды: 50000 руб. в месяц. Срок: с 15.07.2023 по 15.07.2024.
    Контактный телефон: 8 (495) 123-45-67, email: contact@romashka.ru
    """

    print("1. Testing text processing...")
    try:
        result = aggregator.process("text", document_text)
        print("✓ AggregatorAgent.process() works")
        print(f"Cleaned text: {result['cleaned_text'][:100]}...")
        print(f"Agent name: {result['agent_name']}")
        print(f"Reflection results: {list(result['reflection_results'].keys())}")
    except Exception as e:
        print(f"✗ Error in process(): {e}")

    print("\n2. Testing document processing...")
    try:
        structured_data = {
            "document_title": "Contract Agreement",
            "document_type": "contract",
            "date_created": "2024-01-01",
            "counterparty_name": "Company LLC",
            "signatory": "John Doe",
            "jurisdiction": "Russia"
        }

        doc_result = aggregator.process_document(document_text, structured_data)
        print("✓ AggregatorAgent.process_document() works")
        print(f"Analysis sections: {list(doc_result.keys())}")
        print(f"Overall recommendation: {doc_result['overall_status']['recommendation']}")
    except Exception as e:
        print(f"✗ Error in process_document(): {e}")

    print("\n3. Testing status...")
    try:
        status = aggregator.get_status()
        print("✓ AggregatorAgent.get_status() works")
        print(f"Available agents: {list(status['available_agents'].keys())}")
    except Exception as e:
        print(f"✗ Error in get_status(): {e}")

    print("\nAll tests completed!")

if __name__ == "__main__":
    test_aggregator_agent()





