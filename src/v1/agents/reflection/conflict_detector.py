

import re
from typing import List, Dict

class ConflictDetector:
    """
    Детектор логических противоречий или несовместимых утверждений в тексте.
    Применяется к юридическим и нормативным документам.
    """

    contradiction_patterns = [
        (r"\b(не позднее|в течение)\b.*?\bдней\b", r"\b(не ранее|по истечении)\b.*?\bдней\b"),
        (r"\bявляется обязательным\b", r"\bможет не применяться\b"),
        (r"\bобязуется\b.*?\bне\b.*?\bвправе\b", r"\bимеет право\b"),
        (r"\bосуществляется на безвозмездной основе\b", r"\bподлежит оплате\b"),
        # Removed the date pattern to avoid regex backreference issues
    ]

    def __init__(self):
        self.compiled_pairs = [
            (re.compile(p1, re.IGNORECASE), re.compile(p2, re.IGNORECASE))
            for p1, p2 in self.contradiction_patterns
        ]

    def detect(self, text: str) -> List[str]:
        """
        Выявляет потенциальные логические противоречия.
        """
        contradictions = []

        for pattern1, pattern2 in self.compiled_pairs:
            matches1 = pattern1.findall(text)
            matches2 = pattern2.findall(text)
            if matches1 and matches2:
                contradictions.append(
                    f"Противоречие между выражениями: «{pattern1.pattern}» и «{pattern2.pattern}»"
                )

        return contradictions

    def evaluate(self, text: str) -> Dict[str, any]:
        contradictions = self.detect(text)
        return {
            "conflict_detected": bool(contradictions),
            "conflict_descriptions": contradictions,
            "recommendation": (
                "В документе обнаружены потенциальные логические противоречия. Требуется ревизия."
                if contradictions else "OK"
            )
        }

