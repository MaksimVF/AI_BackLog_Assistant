


"""
Test script for the unified ReflectionAgent with integrated pipeline functionality.
"""

from agents.reflection_agent import ReflectionAgent, ReflectionInput

def test_unified_reflection_agent():
    print("Testing Unified ReflectionAgent...")
    print("=" * 50)

    # Create the agent
    reflection_agent = ReflectionAgent()

    # Test data
    contract_text = """
    Настоящий договор аренды заключён между ООО "Ромашка" и ИП Иванов И.И.
    Сумма аренды: 50000 руб. в месяц. Срок: с 15.07.2023 по 15.07.2024.
    Контактный телефон: 8 (495) 123-45-67, email: contact@romashka.ru
    """

    report_text = """
    Ежемесячный отчёт о продажах за январь 2023 года
    Общая выручка: 1 500 000 руб.
    Количество клиентов: 456
    Средний чек: 7 123 руб.
    """

    print("1. Testing standard reflection analysis...")
    reflection_input = ReflectionInput(content=contract_text)
    result = reflection_agent.reflect(reflection_input)
    print(f"Context: {result.context}")
    print(f"Intent: {result.intent}")
    print(f"Next agent: {result.next_agent}")
    print()

    print("2. Testing pipeline processing...")
    pipeline_result = reflection_agent.process_text_with_pipeline(contract_text)
    print(f"Cleaned text: {pipeline_result['cleaned_text'][:100]}...")
    print(f"Entities: {pipeline_result['entities']}")
    print(f"Agent name: {pipeline_result['agent_name']}")
    print(f"Route description: {pipeline_result['route_description']}")
    print()

    print("3. Testing available routes...")
    routes = pipeline_result['available_routes']
    print("Available contextual routes:")
    for route in routes:
        print(f"  - {route['name']}: {route['description']}")
    print()

    print("4. Testing report processing...")
    report_result = reflection_agent.process_text_with_pipeline(report_text)
    print(f"Agent name: {report_result['agent_name']}")
    print(f"Route description: {report_result['route_description']}")
    print()

if __name__ == "__main__":
    test_unified_reflection_agent()


