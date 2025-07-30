




# TODO: Import LLM client when available
# from core.llm.llm_client import llm_chat

class SemanticTaggingAgent:
    """
    SemanticTaggingAgent: Выделяет теги, ключевые понятия, сущности и смысловые маркеры.

    Определяет ключевые теги и сущности, описывающие документ, включая:
    - Юридические термины
    - Финансовые категории
    - Персоналии, организации, документы
    - Географические и временные маркеры
    """

    def __init__(self):
        self.system_prompt = (
            "Ты агент по семантической разметке документа. "
            "Извлеки из текста ключевые теги, термины, имена, даты, названия организаций, "
            "географические объекты и смысловые категории, описывающие документ.\n"
            "Верни результат в виде списка тегов через запятую."
        )

    def extract_tags(self, text: str) -> list:
        """
        Extract semantic tags from the document text.

        Args:
            text: The document text to analyze

        Returns:
            A list of extracted tags
        """
        # TODO: Implement LLM-based semantic tagging when dependencies are available
        # user_prompt = f"Вот содержимое документа:\n{text[:3000]}\n\nВыдели ключевые теги:"
        # response = llm_chat(self.system_prompt, user_prompt)
        # tags = [tag.strip().lower() for tag in response.split(',') if tag.strip()]
        # return tags

        # For now, use simple keyword extraction as placeholder
        text_lower = text.lower()
        words = text_lower.split()

        # Simple keyword-based tagging
        tags = []
        keywords = [
            "договор", "акт", "счет", "счет-фактура", "платёжка", "справка",
            "приказ", "протокол", "трудовой", "устав", "заявление", "отчет",
            "бухгалтерия", "юриспруденция", "медицина", "образование",
            "строительство", "технологии", "финансы", "Москва", "Санкт-Петербург",
            "2023", "2024", "ООО", "ИП", "АО", "ПАО"
        ]

        for word in words:
            if word in keywords and word not in tags:
                tags.append(word)

        return tags



