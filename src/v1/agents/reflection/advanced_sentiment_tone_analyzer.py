




from typing import Dict, Any, List
from agents.llm_client import chat_completion

class AdvancedSentimentAndToneAnalyzer:
    """
    Проводит углубленный анализ тональности и стиля текста с использованием LLM.
    Дополняет базовый StyleAndToneAnalyzer.
    """

    def __init__(self):
        self.name = "AdvancedSentimentAndToneAnalyzer"
        self.system_prompt = (
            "Ты эксперт по анализу тональности и стиля текста. "
            "Проанализируй предоставленный текст и определи:\n"
            "1. Общую тональность (позитивная, негативная, нейтральная)\n"
            "2. Эмоциональную окраску (гнев, радость, грусть, страх, удивление, отвращение)\n"
            "3. Стиль общения (формальный, неформальный, профессиональный, дружеский, агрессивный)\n"
            "4. Уровень уверенности автора (высокий, средний, низкий)\n\n"
            "Ответь в формате JSON с полями: 'sentiment', 'emotions', 'style', 'confidence', 'explanation'."
        )

    def analyze(self, text: str, model_name: str = None) -> dict:
        """
        Анализирует текст по параметрам тональности, стиля и эмоциональной окраски.

        Args:
            text: Текст для анализа
            model_name: Название модели для использования (None для модели по умолчанию)

        Returns:
            Словарь с результатами анализа
        """
        try:
            # Prepare messages for LLM
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Текст для анализа:\n\n{text[:4000]}"}  # Limit to 4000 chars
            ]

            # Call LLM for analysis
            response = chat_completion(messages, model_name=model_name)

            # Try to parse JSON response if possible
            try:
                import json
                result = json.loads(response)
                return {
                    "sentiment_analysis": result,
                    "model_used": model_name or "default",
                    "success": True
                }
            except (json.JSONDecodeError, ValueError):
                # If not valid JSON, return raw response
                return {
                    "sentiment_analysis": {
                        "raw_response": response,
                        "error": "Не удалось обработать ответ модели"
                    },
                    "model_used": model_name or "default",
                    "success": False
                }

        except Exception as e:
            return {
                "sentiment_analysis": {
                    "error": f"Ошибка при анализе тональности: {str(e)}"
                },
                "model_used": model_name or "default",
                "success": False
            }




