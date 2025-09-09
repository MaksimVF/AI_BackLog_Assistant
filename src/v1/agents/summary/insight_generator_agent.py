



"""
Insight Generator Agent
"""

from typing import List
from agents.llm_client import chat_completion

class InsightGeneratorAgent:
    """
    Генерирует аналитические выводы и рекомендации на основе ключевых пунктов.
    """

    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.system_prompt = (
            "Ты эксперт по анализу документов. На основе предоставленных ключевых пунктов "
            "сгенерируй аналитические выводы и практические рекомендации. "
            "Выводы должны быть структурированы и содержать:\n"
            "1. Основные наблюдения\n"
            "2. Потенциальные риски или проблемы\n"
            "3. Конкретные рекомендации по действиям\n\n"
            "Ответь на русском языке в формате разметки Markdown."
        )

    def generate_insights(self, keypoints: list[str]) -> str:
        """
        Generates analytical insights from keypoints.

        Args:
            keypoints: List of key points

        Returns:
            Analytical insights and recommendations
        """
        try:
            # Prepare keypoints text
            keypoints_text = "\n".join(f"- {point}" for point in keypoints)

            # Prepare messages for LLM
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Ключевые пункты для анализа:\n\n{keypoints_text}"}
            ]

            # Call LLM for insight generation
            response = chat_completion(messages, model_name=self.model_name)

            return response.strip()

        except Exception as e:
            # Fallback to placeholder insights if LLM fails
            return (
                f"Ошибка при генерации аналитических выводов: {str(e)}\n\n"
                "ПЛЕЙСХОЛДЕР: Аналитические выводы:\n\n"
                "1. Договор является стандартным соглашением о поставке\n"
                "2. Стороны имеют юридический статус (ООО и ИП)\n"
                "3. Документ относится к московской юрисдикции\n\n"
                "Рекомендации:\n"
                "- Проверить наличие всех необходимых подписей\n"
                "- Убедиться в соответствии условий договора законодательству"
            )



