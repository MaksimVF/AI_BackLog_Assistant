




from typing import List
from agents.llm_client import chat_completion

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

    def extract_tags(self, text: str, use_llm: bool = True, model_name: str = None) -> list:
        """
        Extract semantic tags from the document text.

        Args:
            text: The document text to analyze
            use_llm: Whether to use LLM for tagging (True) or fallback to keyword-based (False)
            model_name: Name of the model to use (None for default model)

        Returns:
            A list of extracted tags
        """
        if use_llm:
            try:
                # Prepare messages for LLM
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Вот содержимое документа:\n{text[:3000]}\n\nВыдели ключевые теги:"}
                ]

                # Call LLM for tag extraction
                response = chat_completion(messages, model_name=model_name)

                # Parse tags from response
                tags = [tag.strip().lower() for tag in response.split(',') if tag.strip()]
                return tags

            except Exception as e:
                # Fallback to keyword-based tagging if LLM fails
                print(f"LLM tagging failed, falling back to keyword-based: {e}")
                return self._keyword_based_tagging(text)
        else:
            return self._keyword_based_tagging(text)

    def _keyword_based_tagging(self, text: str) -> List[str]:
        """Fallback keyword-based tagging method."""
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



