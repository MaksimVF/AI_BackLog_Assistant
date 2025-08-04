

"""
Test script for the new PipelineCoordinatorAgent.
"""

from agents.pipeline_coordinator_agent import PipelineCoordinatorAgent

def test_pipeline_coordinator_agent():
    print("Testing PipelineCoordinatorAgent...")
    print("=" * 50)

    # Create the agent
    coordinator = PipelineCoordinatorAgent()

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
    result = coordinator.process("text", document_text)
    print(f"Cleaned text: {result['cleaned_text'][:100]}...")
    print(f"Agent name: {result['agent_name']}")
    print(f"Summary: {result['reflection_results']['summary']['summary']}")
    print()

    print("2. Testing document processing...")
    doc_result = coordinator.process_document(document_text, structured_data)
    print(f"Overall recommendation: {doc_result['overall_status']['recommendation']}")
    print(f"Issues found: {doc_result['overall_status']['issues_found']}")
    print()

    print("3. Testing routing...")
    routing_result = coordinator.analyze_and_route(document_text)
    print(f"Next agent: {routing_result.next_agent}")
    print(f"Priority: {routing_result.priority}")
    print(f"Reasoning: {routing_result.reasoning}")
    print()

    print("4. Testing status...")
    status = coordinator.get_status()
    print(f"Available agents: {list(status['available_agents'].keys())}")
    print()

if __name__ == "__main__":
    test_pipeline_coordinator_agent()

