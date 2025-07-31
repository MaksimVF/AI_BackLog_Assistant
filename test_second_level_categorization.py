





"""
Test Second Level Categorization
"""

from agents.categorization.second_level_categorization_agent import SecondLevelCategorizationAgent

def test_second_level_categorization():
    """
    Test second level categorization for different domains.
    """
    agent = SecondLevelCategorizationAgent()

    # Test IT domain
    it_document = """
    Ошибка в системе: При попытке сохранить файл возникает исключение NullPointerException.
    Логи показывают, что проблема в модуле FileManager.
    """

    it_result = agent.categorize(it_document, "it")
    print(f"IT Document Result: {it_result}")

    # Test Finance domain
    finance_document = """
    Счёт на оплату №12345 от 2025-01-15.
    Поставщик: ООО "ТехноСервис"
    Сумма: 150,000 рублей
    """

    finance_result = agent.categorize(finance_document, "finance")
    print(f"Finance Document Result: {finance_result}")

    # Test fallback domain
    general_document = """
    Отчёт о выполнении задач за январь 2025 года.
    Все задачи выполнены в срок, за исключением задачи №456.
    """

    general_result = agent.categorize(general_document, "fallback")
    print(f"General Document Result: {general_result}")

    # Verify results
    assert it_result["domain"] == "it"
    assert finance_result["domain"] == "finance"
    assert general_result["domain"] == "fallback"

    print("All tests passed!")

if __name__ == "__main__":
    test_second_level_categorization()





