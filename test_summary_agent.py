


"""
Test Summary Agent
"""

from agents.summary import SummaryAgent

def test_summary_agent():
    """Test the SummaryAgent with a sample document."""

    # Sample document text
    document_text = """
    Договор № 345/2023 от 01.07.2023
    между ООО «Пример» и ИП Иванов

    1. Предмет договора
    Поставщик обязуется поставить товар в соответствии с условиями настоящего договора.

    2. Условия поставки
    Товар должен быть доставлен в г. Москва в течение 10 рабочих дней.

    3. Оплата
    Покупатель обязуется оплатить товар в течение 5 банковских дней после получения.
    """

    print("Testing SummaryAgent...")
    print("Document text:", document_text)
    print("\n" + "="*50 + "\n")

    # Create and test the SummaryAgent
    summary_agent = SummaryAgent()

    # Generate formatted summary
    formatted_summary = summary_agent.generate_formatted_summary(document_text)

    print(formatted_summary)

    print("\n" + "="*50 + "\n")
    print("Test completed successfully!")

if __name__ == "__main__":
    test_summary_agent()



