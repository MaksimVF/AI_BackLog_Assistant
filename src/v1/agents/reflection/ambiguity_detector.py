

import re
from typing import List, Dict

class AmbiguityDetector:
    """
    Выявляет гарантированные расплывчатые, неопределенные или противоречивые формулировки в тексте.
    """

    # Ключевые фразы, указывающие на неопределённость или двусмысленность
    ambiguous_patterns = [
        r"\bпри необходимости\b",
        r"\bпо возможности\b",
        r"\bв разумный срок\b",
        r"\bпо усмотрению\b",
        r"\bиные обстоятельства\b",
        r"\bв исключительных случаях\b",
        r"\bв максимально возможной степени\b",
        r"\bв надлежащем порядке\b",
        r"\bдолжным образом\b",
        r"\bсвоевременно\b"
    ]

    def __init__(self):
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.ambiguous_patterns]

    def detect(self, text: str) -> List[str]:
        """
        Находит все фразы в тексте, соответствующие шаблонам неопределённости.
        """
        matches = []
        for pattern in self.compiled_patterns:
            found = pattern.findall(text)
            matches.extend(found)
        return list(set(matches))

    def evaluate(self, text: str) -> Dict[str, any]:
        matches = self.detect(text)
        return {
            "ambiguity_detected": bool(matches),
            "ambiguous_phrases": matches,
            "recommendation": (
                "Рекомендуется уточнить двусмысленные формулировки" if matches else "OK"
            )
        }

