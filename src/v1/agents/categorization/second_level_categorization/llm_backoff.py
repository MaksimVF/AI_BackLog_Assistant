





"""
LLM Fallback for Categorization
"""

from agents.llm_client import chat_completion

def classify_with_llm(document: str, domain: str) -> dict:
    """
    Uses LLM as fallback when embedding-based categorization fails.

    Args:
        document: The document text to categorize
        domain: The domain context

    Returns:
        Categorization result
    """
    try:
        # Prepare system prompt
        system_prompt = (
            f"Ты являешься классификатором документов в сфере {domain}. "
            "Прочитай документ и предложи краткую категорию, описывающую его тип. "
            "Ответ должен быть одной строкой без пояснений."
        )

        # Prepare messages for LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Документ: {document[:2000]}"}  # Limit to 2000 chars
        ]

        # Call LLM for categorization
        category = chat_completion(messages)

        return {
            "category": category.strip(),
            "confidence": 0.7,  # LLM-based confidence
            "source": "llm"
        }

    except Exception as e:
        # Fallback to placeholder if LLM fails
        return {
            "category": f"llm_{domain}_category",
            "confidence": 0.4,
            "source": "llm",
            "error": f"LLM categorization failed: {str(e)}"
        }





