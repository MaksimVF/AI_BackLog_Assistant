


"""
Test script for report handler integration.
"""

import sys
import os
import logging

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handlers.report_handler import ReportHandler
from agents.reflection_agent.contextual_router import route_text

def test_report_handler():
    """Test the report handler with different types of reports."""

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Test cases
    test_cases = [
        {
            "name": "Sales Report",
            "text": """
            Ежемесячный отчёт о продажах за январь 2023 года
            Общая выручка: 1 500 000 руб.
            Количество клиентов: 456
            Средний чек: 7 123 руб.
            """,
            "expected_type": "sales"
        },
        {
            "name": "Financial Report",
            "text": """
            Годовой финансовый отчёт компании за 2023 год
            Баланс: 5 000 000 руб.
            Прибыль: 1 200 000 руб.
            Убыток: 300 000 руб.
            """,
            "expected_type": "financial"
        },
        {
            "name": "Operational Report",
            "text": """
            Еженедельный операционный отчёт
            Производительность: 95%
            Отклонения: 2%
            Прогноз на следующую неделю: 97%
            """,
            "expected_type": "operational"
        }
    ]

    print("Testing Report Handler...")
    print("=" * 50)

    for test_case in test_cases:
        print(f"\nTest Case: {test_case['name']}")
        print("-" * 30)

        # Test routing
        routed_to = route_text(test_case['text'])
        print(f"Routed to: {routed_to}")

        # Test report handler
        handler = ReportHandler(document_text=test_case['text'])
        result = handler.run()

        print(f"Report Type: {result['subtype']}")
        print(f"Metadata: {result['metadata']}")
        print(f"Text Preview: {result['text'][:100]}...")

        # Verify routing
        if routed_to == "report_handler":
            print("✅ Routing successful")
        else:
            print("❌ Routing failed")

        # Verify report type
        if result['subtype'] == test_case['expected_type']:
            print("✅ Report type classification successful")
        else:
            print(f"❌ Report type classification failed (expected: {test_case['expected_type']}, got: {result['subtype']})")

if __name__ == "__main__":
    test_report_handler()


