


"""
Keypoint Compressor Agent
"""

class KeypointCompressorAgent:
    """
    Преобразует извлечённое содержание документа в краткий список ключевых пунктов.
    """

    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name

    def compress_to_keypoints(self, extracted_summary: str) -> list[str]:
        """
        Converts extracted summary into bullet points.

        Args:
            extracted_summary: The summary text to compress

        Returns:
            List of key points
        """
        # TODO: Implement LLM call for keypoint compression
        # For now, return placeholder keypoints
        return [
            "Договор поставки № 345/2023",
            "Стороны: ООО 'Пример' и ИП Иванов",
            "Предмет: поставка товара",
            "Местоположение: Москва"
        ]


