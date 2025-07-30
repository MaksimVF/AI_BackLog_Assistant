

# test_reflection_agent_router.py

"""
Test script for ReflectionAgent contextual router.
"""

from agents.reflection_agent.contextual_router import route_text, get_all_routes, get_route_description

def test_contextual_router():
    """Test the contextual router with various document types."""

    # Test case 1: Contract text
    contract_text = "Настоящий договор аренды заключён между сторонами..."
    result1 = route_text(contract_text)
    print(f"Contract text routed to: {result1}")
    print(f"Expected: contract_handler")
    print()

    # Test case 2: Invoice text
    invoice_text = "Счёт на оплату №12345 от 01.01.2023 на сумму 10000 рублей"
    result2 = route_text(invoice_text)
    print(f"Invoice text routed to: {result2}")
    print(f"Expected: invoice_handler")
    print()

    # Test case 3: Report text
    report_text = "Ежемесячный отчёт о продажах за январь 2023 года"
    result3 = route_text(report_text)
    print(f"Report text routed to: {result3}")
    print(f"Expected: report_handler")
    print()

    # Test case 4: Generic text
    generic_text = "Привет, как дела? Что нового?"
    result4 = route_text(generic_text)
    print(f"Generic text routed to: {result4}")
    print(f"Expected: generic_handler")
    print()

    # Test route information functions
    print("Available routes:")
    routes = get_all_routes()
    for route in routes:
        desc = get_route_description(route)
        print(f"  - {route}: {desc}")
    print()

    # Test fallback
    empty_text = ""
    result5 = route_text(empty_text)
    print(f"Empty text routed to: {result5}")
    print(f"Expected: generic_handler")

if __name__ == "__main__":
    test_contextual_router()

