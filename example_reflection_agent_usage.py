


# example_reflection_agent_usage.py

"""
Example usage of ReflectionAgent contextual router for document processing.
"""

from agents.reflection_agent.contextual_router import route_text

def main():
    """Demonstrate how to use the contextual router."""

    print("📄 ReflectionAgent: Contextual Document Router")
    print("=" * 50)

    # Example documents
    documents = [
        "Настоящий договор аренды заключён между ООО 'Ромашка' и ИП Иванов И.И.",
        "Счёт на оплату №45678 от 15.07.2023 на сумму 25000 рублей за услуги консалтинга",
        "Квартальный финансовый отчёт компании за 2-й квартал 2023 года",
        "Привет! Напоминаю о встрече завтра в 10:00",
        "Договор поставки оборудования между ООО 'Техно' и ООО 'Прогресс'"
    ]

    # Process each document
    for i, doc in enumerate(documents, 1):
        agent = route_text(doc)
        print(f"Документ {i}: {doc[:50]}...")
        print(f"  → Направлен агенту: {agent}")
        print()

    print("Все документы успешно маршрутизированы!")

if __name__ == "__main__":
    main()


