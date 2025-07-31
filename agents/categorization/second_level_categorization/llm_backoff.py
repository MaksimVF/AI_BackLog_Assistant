





"""
LLM Fallback for Categorization
"""

def classify_with_llm(document: str, domain: str) -> dict:
    """
    Uses LLM as fallback when embedding-based categorization fails.

    Args:
        document: The document text to categorize
        domain: The domain context

    Returns:
        Categorization result
    """
    # TODO: Implement actual LLM call
    # For now, return a placeholder result

    # This would be the prompt for LLM:
    # prompt = f"""
    # Ты являешься классификатором документов в сфере {domain}.
    # Прочитай документ и предложи краткую категорию, описывающую его тип.
    # Ответ должен быть одной строкой без пояснений.
    # Документ: {document}
    # """.strip()

    # For demonstration, we'll return a placeholder
    return {
        "category": f"llm_{domain}_category",
        "confidence": 0.4,
        "source": "llm"
    }





