



from typing import List
from agents.llm_client import chat_completion

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
            "Выбери одну из сфер: ['бухгалтерия', 'юриспруденция', 'медицина', 'образование', 'строительство', 'технологии', 'финансы', 'прочее'].\n"
            "Ответь только названием сферы, без дополнительного текста."
        )

    def classify(self, text: str, use_llm: bool = True, model_name: str = None) -> str:
        """
        Classify the document domain based on its content.

        Args:
            text: The document text to classify
            use_llm: Whether to use LLM for classification (True) or fallback to keyword-based (False)
            model_name: Name of the model to use (None for default model)

        Returns:
            The domain as a string
        """
        if use_llm:
            try:
                # Prepare messages for LLM
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Вот содержимое документа:\n{text[:3000]}\n\nОпредели сферу деятельности:"}
                ]

                # Call LLM for classification
                response = chat_completion(messages, model_name=model_name)

                # Clean and return the response
                domain = response.strip().lower()
                # Validate that it's one of the expected domains
                valid_domains = ['бухгалтерия', 'юриспруденция', 'медицина', 'образование', 'строительство', 'технологии', 'финансы', 'прочее']
                if domain in valid_domains:
                    return domain
                else:
                    # If LLM returns invalid domain, fallback to keyword-based
                    print(f"LLM returned invalid domain '{domain}', falling back to keyword-based")
                    return self._keyword_based_classification(text)

            except Exception as e:
                print(f"LLM classification failed, falling back to keyword-based: {e}")
                return self._keyword_based_classification(text)
        else:
            return self._keyword_based_classification(text)

    def _keyword_based_classification(self, text: str) -> str:
        """Fallback keyword-based classification method."""
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



