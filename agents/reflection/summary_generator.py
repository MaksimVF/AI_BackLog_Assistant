




from core.llm_client import chat_completion

class SummaryGenerator:
    """
    Генерирует краткое резюме документа с сохранением ключевых фактов и смысла.
    """

    def __init__(self):
        self.name = "SummaryGenerator"

    def generate_summary(self, text: str) -> dict:
        """
        Создает краткое резюме текста.
        """
        prompt = (
            "Создай краткое резюме следующего текста, сохраняя ключевые факты и смысл. "
            "Используй нейтральный и точный стиль.\n\n"
            f"{text}"
        )
        response = chat_completion(prompt)
        return {"summary": response}




