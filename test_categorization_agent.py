


from agents.categorization.categorization_agent import CategorizationAgent

def test_categorization_agent():
    """Test the CategorizationAgent with different types of documents."""

    categorizer = CategorizationAgent()

    # Test 1: Contract document
    contract_text = "Договор № 345/2023 от 01.07.2023 между ООО «Пример» и ИП Иванов о поставке товаров"
    result = categorizer.categorize(contract_text)
    print("Contract categorization:")
    print(result)
    print()

    # Test 2: Invoice document
    invoice_text = "Счет на оплату № 12345 от 15.08.2023 на сумму 120 000,00 руб"
    result = categorizer.categorize(invoice_text)
    print("Invoice categorization:")
    print(result)
    print()

    # Test 3: Medical report
    medical_text = "Медицинское заключение пациента Иванова И.И. от 10.09.2023"
    result = categorizer.categorize(medical_text)
    print("Medical report categorization:")
    print(result)
    print()

    # Test 4: Technology document
    tech_text = "Техническое задание на разработку программного обеспечения для автоматизации бизнес-процессов"
    result = categorizer.categorize(tech_text)
    print("Technology document categorization:")
    print(result)
    print()

if __name__ == "__main__":
    test_categorization_agent()


