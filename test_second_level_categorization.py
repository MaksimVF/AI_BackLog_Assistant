





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

    # Test Legal domain
    legal_document = """
    Договор аренды №789 от 2025-02-20.
    Арендодатель: ООО "Недвижимость Плюс"
    Арендатор: ИП Иванов И.И.
    """

    legal_result = agent.categorize(legal_document, "legal")
    print(f"Legal Document Result: {legal_result}")

    # Test Healthcare domain
    healthcare_document = """
    Результаты анализа крови пациента Иванова И.И.
    Гемоглобин: 140 г/л, Лейкоциты: 6.5 x 10^9/л
    """

    healthcare_result = agent.categorize(healthcare_document, "healthcare")
    print(f"Healthcare Document Result: {healthcare_result}")

    # Test Personal Growth domain
    personal_growth_document = """
    Мои цели на 2025 год:
    1. Выучить английский язык до уровня B2
    2. Прочитать 24 книги
    3. Начать заниматься йогой
    """

    personal_growth_result = agent.categorize(personal_growth_document, "personal_growth")
    print(f"Personal Growth Document Result: {personal_growth_result}")

    # Test Customer Support domain
    customer_support_document = """
    Уважаемая поддержка,
    Я не могу войти в свой аккаунт. Проблема с восстановлением пароля.
    """

    customer_support_result = agent.categorize(customer_support_document, "customer_support")
    print(f"Customer Support Document Result: {customer_support_result}")

    # Test Project Management domain
    project_management_document = """
    План проекта "Разработка мобильного приложения":
    1. Анализ требований - 2 недели
    2. Дизайн интерфейса - 3 недели
    3. Разработка - 8 недель
    """

    project_management_result = agent.categorize(project_management_document, "project_management")
    print(f"Project Management Document Result: {project_management_result}")

    # Test fallback domain
    general_document = """
    Отчёт о выполнении задач за январь 2025 года.
    Все задачи выполнены в срок, за исключением задачи №456.
    """

    general_result = agent.categorize(general_document, "fallback")
    print(f"General Document Result: {general_result}")

    # Test categorization with fallback
    print("\n--- Testing LLM Fallback ---")
    agent_with_fallback = SecondLevelCategorizationAgent(confidence_threshold=0.8)

    # Test with a document that might have low confidence
    ambiguous_document = """
    Это документ с неясным содержанием, который может быть трудно классифицировать.
    Он содержит элементы из разных категорий.
    """

    fallback_result = agent_with_fallback.categorize_with_fallback(ambiguous_document, "it")
    print(f"Fallback Result: {fallback_result}")

    # Verify results
    assert it_result["domain"] == "it"
    assert finance_result["domain"] == "finance"
    assert legal_result["domain"] == "legal"
    assert healthcare_result["domain"] == "healthcare"
    assert personal_growth_result["domain"] == "personal_growth"
    assert customer_support_result["domain"] == "customer_support"
    assert project_management_result["domain"] == "project_management"
    assert general_result["domain"] == "fallback"

    # Verify that fallback result has expected structure
    assert "domain" in fallback_result
    assert "category" in fallback_result
    assert "confidence" in fallback_result
    assert "source" in fallback_result

    print("All tests passed!")

if __name__ == "__main__":
    test_second_level_categorization()





