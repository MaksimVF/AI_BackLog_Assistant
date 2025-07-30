


# test_entity_extractor.py

"""
Test script for the entity extractor module.
"""

from agents.analyzers.entity_extractor import EntityExtractor

def test_entity_extractor():
    """Test the entity extractor with various document types."""

    extractor = EntityExtractor()

    # Test case 1: Contract with dates, organizations, and amounts
    contract_text = """
    Настоящий договор аренды №123 заключён между ООО "Ромашка" и ИП Иванов И.И.
    Дата заключения: 15.07.2023. Сумма аренды: 50000 руб. ежемесячно.
    Контактный телефон: +7 (123) 456-78-90, email: contact@romashka.ru
    """

    print("Test Case 1: Contract")
    print("=" * 50)
    entities1 = extractor.extract(contract_text)
    print_entities(entities1)
    print()

    # Test case 2: Invoice with amounts and dates
    invoice_text = """
    Счёт на оплату №45678 от 20.08.2023
    ООО "ТехноСервис" (ИНН 1234567890)
    Сумма к оплате: 12500.50 руб.
    Оплатить до: 30.08.2023
    """

    print("Test Case 2: Invoice")
    print("=" * 50)
    entities2 = extractor.extract(invoice_text)
    print_entities(entities2)
    print()

    # Test case 3: Report with various entities
    report_text = """
    Квартальный отчёт за 1-й квартал 2023 года
    Подготовлено: ООО "Аналитика Плюс"
    Общая выручка: 1 500 000 руб. (рост на 15% по сравнению с предыдущим кварталом)
    Контакт для вопросов: +7 123 456 78 90, info@analytica.ru
    """

    print("Test Case 3: Report")
    print("=" * 50)
    entities3 = extractor.extract(report_text)
    print_entities(entities3)
    print()

    # Test case 4: Text with phone numbers and emails
    contact_text = """
    Контактная информация:
    Телефон: 8 (495) 123-45-67
    Мобильный: +79123456789
    Email: support@example.com
    Альтернативный email: info@company.ru
    """

    print("Test Case 4: Contacts")
    print("=" * 50)
    entities4 = extractor.extract(contact_text)
    print_entities(entities4)
    print()

def print_entities(entities):
    """Print extracted entities in a readable format."""
    for entity_type, values in entities.items():
        if values:
            print(f"{entity_type.capitalize()}: {', '.join(values)}")
        else:
            print(f"{entity_type.capitalize()}: None")

if __name__ == "__main__":
    test_entity_extractor()


