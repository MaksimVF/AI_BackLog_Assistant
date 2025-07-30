

"""
Document classification module for determining document types.
This module can be used independently or integrated into the contextual router.
"""

from typing import List, Dict, Any

def classify(text: str, tables: List[dict]) -> str:
    """
    Determines document type based on keywords and table structure.
    Returns one of: 'report', 'contract', 'unknown'.

    Args:
        text: The text content of the document
        tables: List of tables extracted from the document

    Returns:
        Document type classification
    """
    text_lower = text.lower()

    report_keywords = [
        "отчёт", "отчет", "бухгалтерский баланс", "прибыль", "убытки",
        "движение денежных средств", "финансовый результат", "счета", "остатки"
    ]

    contract_keywords = [
        "договор", "стороны", "обязанности", "права", "срок действия",
        "предмет договора", "исполнитель", "заказчик", "ответственность", "реквизиты"
    ]

    if tables and any(kw in text_lower for kw in report_keywords):
        return "report"
    elif any(kw in text_lower for kw in contract_keywords):
        return "contract"
    else:
        return "unknown"

def classify_with_details(text: str, tables: List[dict]) -> Dict[str, Any]:
    """
    Extended classification that returns additional metadata.

    Args:
        text: The text content of the document
        tables: List of tables extracted from the document

    Returns:
        Dictionary with classification result and metadata
    """
    classification = classify(text, tables)

    # Additional metadata extraction
    metadata = {
        "has_tables": bool(tables),
        "table_count": len(tables) if tables else 0,
        "confidence": 0.9 if classification != "unknown" else 0.5
    }

    return {
        "classification": classification,
        "metadata": metadata
    }

