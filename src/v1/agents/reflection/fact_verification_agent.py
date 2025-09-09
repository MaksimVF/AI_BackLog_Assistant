



from typing import Dict, Any, List
from agents.llm_client import chat_completion

class FactVerificationAgent:
    """
    Проверяет фактическую точность утверждений в тексте с использованием LLM.
    """

    def __init__(self):
        self.name = "FactVerificationAgent"
        self.system_prompt = (
            "Ты эксперт по проверке фактов. "
            "Проанализируй следующий текст и выяви любые фактические ошибки или неточности. "
            "Ответь в формате JSON с полями: 'factually_correct' (bool), 'issues' (list of strings), 'confidence' (float 0-1)."
        )

    def verify_facts(self, text: str, model_name: str = None) -> dict:
        """
        Проверяет текст на наличие фактических ошибок.

        Args:
            text: Текст для проверки
            model_name: Название модели для использования (None для модели по умолчанию)

        Returns:
            Результат проверки фактов
        """
        try:
            # Prepare messages for LLM
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Текст для проверки:\n\n{text[:3000]}"}  # Limit to 3000 chars
            ]

            # Call LLM for fact verification
            response = chat_completion(messages, model_name=model_name)

            # Try to parse JSON response if possible
            try:
                import json
                result = json.loads(response)
                return {
                    "verification_results": result,
                    "model_used": model_name or "default"
                }
            except (json.JSONDecodeError, ValueError):
                # If not valid JSON, return raw response
                return {
                    "verification_results": {
                        "factually_correct": None,
                        "issues": ["Не удалось обработать ответ модели"],
                        "confidence": 0.0,
                        "raw_response": response
                    },
                    "model_used": model_name or "default"
                }

        except Exception as e:
            return {
                "verification_results": {
                    "factually_correct": None,
                    "issues": [f"Ошибка при проверке фактов: {str(e)}"],
                    "confidence": 0.0
                },
                "model_used": model_name or "default"
            }



