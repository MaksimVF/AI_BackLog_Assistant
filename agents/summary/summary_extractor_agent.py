

"""
Summary Extractor Agent
"""

from agents.llm_client import chat_completion

class SummaryExtractorAgent:
    """
    Извлекает основное содержание документа — ключевые идеи, факты, события.
    """

    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.system_prompt = (
            "Ты эксперт по извлечению ключевой информации из документов. "
            "Проанализируй предоставленный текст и выдели основное содержание: "
            "ключевые идеи, факты, события и важные детали. "
            "Представь результат в виде маркированного списка на русском языке."
        )

    def extract_summary(self, document_text: str) -> str:
        """
        Extracts the main content from a document.

        Args:
            document_text: The text of the document to summarize

        Returns:
            A summary of the document's main content
        """
        try:
            # Prepare messages for LLM
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Текст документа для анализа:\n\n{document_text[:8000]}"}  # Limit to 8000 chars
            ]

            # Call LLM for summary extraction
            response = chat_completion(messages, model_name=self.model_name)

            return response.strip()

        except Exception as e:
            # Fallback to placeholder response if LLM fails
            return (
                f"Ошибка при извлечении основного содержания: {str(e)}\n\n"
                "ПЛЕЙСХОЛДЕР: Основное содержание документа:\n"
                "- Документ содержит информацию о договоре поставки\n"
                "- Ключевые стороны: ООО 'Пример' и ИП Иванов\n"
                "- Основные условия: поставка товара в Москве"
            )

