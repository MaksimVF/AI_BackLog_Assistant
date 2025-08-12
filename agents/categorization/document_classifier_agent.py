


from typing import Dict, Any, List, Optional, Union
from agents.llm_client import chat_completion
from utils.batch_decorator import batch_processing

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

    @batch_processing(agent_type="classifier", batch_size=3, max_wait_time=1.0)
    def classify(self, text: str, model_name: str = None, use_llm: bool = True) -> str:
        """
        Classify the document type based on its content.

        This method supports batch processing for improved efficiency when
        classifying multiple documents.

        Args:
            text: The document text to classify
            model_name: Optional model name to use (None for default)
            use_llm: Whether to use LLM for classification (True) or fallback to heuristics (False)

        Returns:
            The document type as a string
        """
        if use_llm:
            try:
                # Prepare messages for LLM
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Вот текст документа:\n{text[:3000]}\n\nКакой это тип документа?"}
                ]

                # Call LLM for classification
                response = chat_completion(messages, model_name=model_name)
                return response.strip().lower()

            except Exception as e:
                # Fallback to heuristic method if LLM fails
                print(f"LLM classification failed, using fallback: {e}")
                return self._classify_with_heuristics(text)
        else:
            return self._classify_with_heuristics(text)

    def _classify_with_heuristics(self, text: str) -> str:
        """Fallback classification using simple keyword matching."""
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


