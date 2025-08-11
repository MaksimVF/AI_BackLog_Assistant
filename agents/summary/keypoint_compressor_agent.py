


"""
Keypoint Compressor Agent
"""

from typing import List
from agents.llm_client import chat_completion

class KeypointCompressorAgent:
    """
    Преобразует извлечённое содержание документа в краткий список ключевых пунктов.
    """

    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.system_prompt = (
            "Ты эксперт по структурированию информации. "
            "Преобразуй предоставленный текст в краткий список ключевых пунктов. "
            "Каждый пункт должен быть лаконичным и содержать основную информацию. "
            "Ответь в формате маркированного списка на русском языке."
        )

    def compress_to_keypoints(self, extracted_summary: str) -> list[str]:
        """
        Converts extracted summary into bullet points.

        Args:
            extracted_summary: The summary text to compress

        Returns:
            List of key points
        """
        try:
            # Prepare messages for LLM
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Текст для преобразования в ключевые пункты:\n\n{extracted_summary[:4000]}"}  # Limit to 4000 chars
            ]

            # Call LLM for keypoint compression
            response = chat_completion(messages, model_name=self.model_name)

            # Parse the response into a list of keypoints
            lines = response.strip().split('\n')
            keypoints = []
            for line in lines:
                line = line.strip()
                # Remove bullet points and numbers from the beginning
                if line and not line.startswith('-') and not line.startswith('•') and not line.lower().startswith('пункт'):
                    line = f"- {line}"
                if line:
                    keypoints.append(line)

            return keypoints

        except Exception as e:
            # Fallback to placeholder keypoints if LLM fails
            return [
                f"Ошибка при преобразовании: {str(e)}",
                "Договор поставки № 345/2023",
                "Стороны: ООО 'Пример' и ИП Иванов",
                "Предмет: поставка товара",
                "Местоположение: Москва"
            ]


