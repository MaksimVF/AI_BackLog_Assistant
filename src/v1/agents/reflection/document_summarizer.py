





from typing import Dict, Any, List, Optional
from agents.llm_client import chat_completion
from agents.base import BaseAgent

class DocumentSummarizer(BaseAgent):
    """
    Генерирует краткое резюме документа с сохранением ключевых фактов и смысла.
    """

    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the DocumentSummarizer.

        Args:
            model_name: Specific model to use (None to use agent's default model)
        """
        super().__init__(name="DocumentSummarizer", model_name=model_name)
        self.system_prompt = (
            "Ты эксперт по созданию кратких резюме документов. "
            "На основе предоставленного текста создай краткое резюме, сохраняя ключевые факты и основной смысл. "
            "Резюме должно быть на том же языке, что и оригинальный текст, и составлять около 20-25% от исходной длины."
        )

    def generate_summary(self, text: str, model_name: Optional[str] = None) -> dict:
        """
        Создает краткое резюме текста.

        Args:
            text: Исходный текст для резюмирования
            model_name: Название модели для использования (None для модели агента)

        Returns:
            Словарь с результатом резюмирования
        """
        try:
            # Prepare messages for LLM
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Текст для резюмирования:\n\n{text[:8000]}"}  # Limit to 8000 chars
            ]

            # Call LLM for summary generation using agent's model by default
            response = chat_completion(messages, model_name=model_name, agent=self)

            return {
                "summary": response.strip(),
                "model_used": model_name or self.get_model_name() or "default",
                "success": True
            }

        except Exception as e:
            return {
                "summary": f"Ошибка при генерации резюме: {str(e)}",
                "model_used": model_name or self.get_model_name() or "default",
                "success": False
            }





