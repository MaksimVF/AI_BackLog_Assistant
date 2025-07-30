



# TODO: Import LLM client when available
# from core.llm.llm_client import llm_chat

class DomainClassifierAgent:
    """
    DomainClassifierAgent: Определяет предметную область документа.

    На основе текста документа определяет сферу деятельности, к которой он относится.
    Это необходимо для назначения специализированных downstream-агентов и подгрузки соответствующих инструкций.
    """

    def __init__(self):
        self.system_prompt = (
            "Ты помощник по определению тематической сферы документа. "
            "На основе содержимого укажи, к какой сфере деятельности он относится.\n"
            "Выбери одну из сфер: ['бухгалтерия', 'юриспруденция', 'медицина', 'образование', 'строительство', 'технологии', 'финансы', 'прочее']."
        )

    def classify(self, text: str) -> str:
        """
        Classify the document domain based on its content.

        Args:
            text: The document text to classify

        Returns:
            The domain as a string
        """
        # TODO: Implement LLM-based domain classification when dependencies are available
        # user_prompt = f"Вот содержимое документа:\n{text[:3000]}\n\nОпредели сферу деятельности:"
        # response = llm_chat(self.system_prompt, user_prompt)
        # return response.strip().lower()

        # For now, use simple keyword matching as placeholder
        text_lower = text.lower()

        if "бухгалтер" in text_lower or "счет" in text_lower or "финанс" in text_lower:
            return "бухгалтерия"
        elif "юридич" in text_lower or "договор" in text_lower or "закон" in text_lower:
            return "юриспруденция"
        elif "медиц" in text_lower or "здравоохранение" in text_lower or "пациент" in text_lower:
            return "медицина"
        elif "образован" in text_lower or "учеб" in text_lower or "студент" in text_lower:
            return "образование"
        elif "строительств" in text_lower or "проект" in text_lower or "объект" in text_lower:
            return "строительство"
        elif "технолог" in text_lower or "IT" in text_lower or "разработк" in text_lower:
            return "технологии"
        elif "финанс" in text_lower or "инвест" in text_lower or "банк" in text_lower:
            return "финансы"
        else:
            return "прочее"



