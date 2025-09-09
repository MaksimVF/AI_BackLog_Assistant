

from typing import List, Dict
from collections import Counter

class RedundancyDetector:
    """
    Анализирует повторяющуюся или избыточную информацию в текстовых блоках документа.
    """

    def __init__(self, repetition_threshold: int = 3):
        # Настраиваемый порог повторений
        self.repetition_threshold = repetition_threshold

    def _normalize(self, text: str) -> str:
        return text.lower().strip()

    def detect_redundancy(self, text_blocks: List[str]) -> Dict[str, int]:
        """
        Находит дублирующиеся блоки текста и возвращает их количество.
        """
        normalized_blocks = [self._normalize(block) for block in text_blocks if block.strip()]
        counter = Counter(normalized_blocks)
        redundant = {block: count for block, count in counter.items() if count >= self.repetition_threshold}
        return redundant

    def evaluate(self, text_blocks: List[str]) -> Dict[str, any]:
        redundant_blocks = self.detect_redundancy(text_blocks)
        return {
            "redundant_blocks_found": bool(redundant_blocks),
            "redundant_blocks": redundant_blocks,
            "recommendation": (
                "Перепроверить повторяющиеся блоки на предмет избыточности"
                if redundant_blocks else "OK"
            )
        }

