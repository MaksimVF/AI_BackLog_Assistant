



"""
Test Self-Learning Categorization
"""

from agents.categorization.second_level_categorization_agent import SecondLevelCategorizationAgent

def test_self_learning_categorization():
    """
    Test self-learning categorization functionality.
    """
    print("=== Testing Self-Learning Categorization ===")

    # Create agent with learning enabled
    agent = SecondLevelCategorizationAgent(confidence_threshold=0.7, enable_learning=True)

    # Test documents for different domains
    test_cases = [
        {
            "domain": "it",
            "documents": [
                "Ошибка в системе: При попытке сохранить файл возникает исключение NullPointerException.",
                "Требования к новому API: Должен поддерживать REST и возвращать JSON.",
                "Запрос на новую функцию: Нужна возможность экспорта данных в Excel."
            ]
        },
        {
            "domain": "finance",
            "documents": [
                "Счёт на оплату №12345 от 2025-01-15. Сумма: 150,000 рублей.",
                "Отчёт о доходах за квартал: Прибыль увеличилась на 15%.",
                "Заявка на кредит: Сумма 500,000 рублей, срок 5 лет."
            ]
        }
    ]

    # First round - categorize documents
    print("\n--- First Round Categorization ---")
    for case in test_cases:
        domain = case["domain"]
        print(f"\nDomain: {domain}")

        for i, doc in enumerate(case["documents"]):
            result = agent.categorize(doc, domain)
            print(f"Doc {i+1}: {result['category']} (conf: {result['confidence']:.3f})")

    # Retrain categorizers
    print("\n--- Retraining Categorizers ---")
    success_count = agent.retrain_all_categorizers()
    print(f"Successfully retrained {success_count} categorizers")

    # Second round - categorize documents after retraining
    print("\n--- Second Round Categorization (After Retraining) ---")
    for case in test_cases:
        domain = case["domain"]
        print(f"\nDomain: {domain}")

        for i, doc in enumerate(case["documents"]):
            result = agent.categorize(doc, domain)
            print(f"Doc {i+1}: {result['category']} (conf: {result['confidence']:.3f})")

    # Test retraining individual domain
    print("\n--- Testing Individual Domain Retraining ---")
    it_retrained = agent.retrain_categorizer("it")
    print(f"IT domain retrained: {it_retrained}")

    print("\n=== Self-Learning Test Completed ===")

if __name__ == "__main__":
    test_self_learning_categorization()


