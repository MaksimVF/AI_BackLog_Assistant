
"""
Test cases for the pipeline aggregator.
"""

from agents.agent_2.pipeline_aggregator import PipelineAggregator

def test_pipeline_aggregator():
    """Test the pipeline aggregator with different document types."""

    pipeline = PipelineAggregator()

    # Test case 1: Contract
    contract_text = """
    Настоящий договор аренды заключён между ООО "Ромашка" и ИП Иванов И.И.
    Сумма аренды: 50000 руб. в месяц. Срок: с 15.07.2023 по 15.07.2024.
    Контактный телефон: 8 (495) 123-45-67, email: contact@romashka.ru
    """

    result1 = pipeline.process(contract_text)
    print("Test Case 1: Contract")
    print("=" * 50)
    print(f"Agent: {result1['agent_name']}")
    print(f"Entities: {result1['entities']}")
    print()

    # Test case 2: Invoice
    invoice_text = """
    Счёт на оплату №12345 от 20.08.2023
    Поставщик: ООО "Техносервис"
    Сумма: 45678 руб.
    Срок оплаты: до 30.08.2023
    """

    result2 = pipeline.process(invoice_text)
    print("Test Case 2: Invoice")
    print("=" * 50)
    print(f"Agent: {result2['agent_name']}")
    print(f"Entities: {result2['entities']}")
    print()

    # Test case 3: Report
    report_text = """
    Ежемесячный отчёт о продажах за январь 2023 года
    Общая выручка: 1 500 000 руб.
    Количество клиентов: 456
    Средний чек: 7 123 руб.
    """

    result3 = pipeline.process(report_text)
    print("Test Case 3: Report")
    print("=" * 50)
    print(f"Agent: {result3['agent_name']}")
    print(f"Entities: {result3['entities']}")
    print()

    # Test case 4: Generic text
    generic_text = """
    Привет, как дела? Что нового в проекте?
    """

    result4 = pipeline.process(generic_text)
    print("Test Case 4: Generic Text")
    print("=" * 50)
    print(f"Agent: {result4['agent_name']}")
    print(f"Entities: {result4['entities']}")
    print()

    # Test batch processing
    texts = [contract_text, invoice_text, report_text, generic_text]
    batch_results = pipeline.process_batch(texts)

    print("Batch Processing Results:")
    print("=" * 50)
    for i, result in enumerate(batch_results, 1):
        print(f"Text {i}: {result['agent_name']}")

    # Test available agents
    print("\nAvailable Agents:")
    print("=" * 50)
    agents = pipeline.get_available_agents()
    for agent in agents:
        description = pipeline.get_agent_description(agent)
        print(f"{agent}: {description}")

if __name__ == "__main__":
    test_pipeline_aggregator()
