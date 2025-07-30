

# agents/agent_2/contextual_router.py

"""
Contextual router for semantic routing of text to appropriate sub-agents.
This module uses the semantic_router package for embedding-based text classification.
"""

from semantic_router import Route, SemanticRouter
from semantic_router.encoders import FastEmbedEncoder
from typing import List, Optional

# Define routes for different document types with example utterances
ROUTES = [
    Route(
        name="invoice_handler",
        utterances=[
            "Счёт на оплату №12345 от 01.01.2023 на сумму 10000 рублей",
            "Акт выполненных работ за январь 2023 года",
            "Накладная на товар от 15.02.2023",
            "Счёт-фактура №789 от 20.03.2023"
        ],
        description="Анализ и структурирование счётов, актов, накладных"
    ),
    Route(
        name="contract_handler",
        utterances=[
            "Настоящий договор аренды заключён между сторонами",
            "Договор поставки товара от 10.04.2023",
            "Соглашение о конфиденциальности",
            "Договор подряда на строительство"
        ],
        description="Обработка договоров и соглашений"
    ),
    Route(
        name="report_handler",
        utterances=[
            "Ежемесячный отчёт о продажах за январь 2023 года",
            "Годовой финансовый отчёт компании",
            "Сводный отчёт по проекту за квартал",
            "Аналитический отчёт по рынку",
            "Отчёт о прибылях и убытках",
            "Баланс компании за 2023 год",
            "Отчёт по KPI за первый квартал",
            "Производственный отчёт за неделю",
            "Отчёт из CRM системы",
            "Отчёт из 1С за месяц",
            "Финансовая сводка за период",

            "Операционный отчёт по подразделению",
            "Еженедельный операционный отчёт",
            "Отчёт по производительности",
            "Отчёт по эффективности",
            "Отчёт по отклонениям",
            "Отчёт по прогнозам"

        ],
        description="Анализ отчётных и сводных документов"
    ),
    Route(
        name="generic_handler",
        utterances=[
            "Привет, как дела?",
            "Что нового?",
            "Обсуждение общего характера",
            "Просто текст без конкретной структуры"
        ],
        description="Обработка общего текста без конкретной структуры"
    )
]

# Create encoder
encoder = FastEmbedEncoder()

# Create router with encoder
router = SemanticRouter(encoder=encoder)

# Add routes to the router
for route in ROUTES:
    router.add(route)



def get_all_routes() -> List[Route]:
    """
    Get all available routes.

    Returns:
        List of Route objects
    """
    # Make sure we're returning the global ROUTES variable
    global ROUTES
    return ROUTES

def get_route_description(route_name: str) -> str:
    """
    Get description for a specific route.

    Args:
        route_name: Name of the route

    Returns:
        Description of the route
    """
    for route in ROUTES:
        if route.name == route_name:
            return route.description
    return "Unknown route"

def route_text(text: str) -> str:

    """
    Determine the most appropriate sub-agent for the given text.
    Returns the route name (sub-agent name).

    Args:
        text: Input text to route

    Returns:
        Name of the sub-agent route
    """
    if not text.strip():
        return "generic_handler"

    match = router(text)
    return match.name if match else "generic_handler"

def get_all_routes() -> List[str]:
    """
    Get a list of all available route names.

    Returns:
        List of route names
    """
    return [route.name for route in ROUTES]

def get_route_description(route_name: str) -> Optional[str]:
    """
    Get the description for a specific route.

    Args:
        route_name: Name of the route

    Returns:
        Description of the route or None if not found
    """
    for route in ROUTES:
        if route.name == route_name:
            return route.description
    return None

