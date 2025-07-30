


# TODO: Import LLM client when available
# from core.llm.llm_client import llm_chat

class DocumentClassifierAgent:
    """
    DocumentClassifierAgent: Определяет тип документа.

    На вход получает текст документа и на выходе возвращает один из предопределённых типов документа.
    В перспективе — может обучаться или использовать внешние модели, а пока работает по эвристикам и LLM-подсказке.
    """

    def __init__(self):
        self.system_prompt = (
            "Ты помощник по классификации документов. "
            "На основе текста определи тип документа. "
            "Возможные типы: ['договор', 'акт', 'счет', 'счет-фактура', 'платёжка', 'справка', "
            "'приказ', 'протокол', 'трудовой договор', 'устав', 'заявление', 'отчет', 'иное'].\n"
            "Отвечай строго одним из указанных вариантов."
        )

    def classify(self, text: str) -> str:
        """
        Classify the document type based on its content.

        Args:
            text: The document text to classify

        Returns:
            The document type as a string
        """
        # TODO: Implement LLM-based classification when dependencies are available
        # user_prompt = f"Вот текст документа:\n{text[:3000]}\n\nКакой это тип документа?"
        # response = llm_chat(self.system_prompt, user_prompt)
        # return response.strip().lower()

        # For now, use simple keyword matching as placeholder
        text_lower = text.lower()

        if "договор" in text_lower:
            return "договор"
        elif "акт" in text_lower:
            return "акт"
        elif "счет" in text_lower:
            return "счет"
        elif "счет-фактура" in text_lower:
            return "счет-фактура"
        elif "платёжка" in text_lower:
            return "платёжка"
        elif "справка" in text_lower:
            return "справка"
        elif "приказ" in text_lower:
            return "приказ"
        elif "протокол" in text_lower:
            return "протокол"
        elif "трудовой договор" in text_lower:
            return "трудовой договор"
        elif "устав" in text_lower:
            return "устав"
        elif "заявление" in text_lower:
            return "заявление"
        elif "отчет" in text_lower:
            return "отчет"
        else:
            return "иное"


