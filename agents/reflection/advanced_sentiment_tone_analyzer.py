



from core.llm_client import chat_completion

class AdvancedSentimentAndToneAnalyzer:
    """
    Проводит углубленный анализ тональности и стиля текста с использованием LLM.
    Дополняет базовый StyleAndToneAnalyzer.
    """

    def __init__(self):
        self.name = "AdvancedSentimentAndToneAnalyzer"

    def analyze(self, text: str) -> dict:
        """
        Анализирует текст по параметрам тональности, стиля и эмоциональной окраски.
        """
        prompt = (
            "Проанализируй текст по следующим параметрам:\n"
            "- Эмоциональная тональность (позитивная, негативная, нейтральная)\n"
            "- Стиль (формальный, разговорный, технический и т.д.)\n"
            "- Наличие эмоционально окрашенных выражений\n\n"
            f"Текст:\n{text}"
        )
        response = chat_completion(prompt)
        return {"sentiment_analysis": response}



