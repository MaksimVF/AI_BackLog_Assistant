


from typing import Dict, Any
import re

class StyleAndToneAnalyzer:
    """
    Анализирует стиль и тональность наличия документа:
    - определяет официально-деловой стиль,
    - выявляет излишнюю эмоциональность, просторечия, жаргон,
    - наконец соответствие формату делового документа.
    """

    # Пример ключевых слов и фраз официально-делового стиля
    official_phrases = [
        r"\bв соответствии с\b",
        r"\bнастоящим документом\b",
        r"\bв целях\b",
        r"\bосуществлять\b",
        r"\bнаправлять\b",
        r"\bсогласно\b",
        r"\bсведения\b",
        r"\bсроки\b",
        r"\bприложение\b",
        r"\bдолжностное лицо\b",
    ]

    # Пример нежелательных разговорных слов и выражений
    informal_phrases = [
        r"\bкороче\b",
        r"\bтипо\b",
        r"\bчётко\b",
        r"\bкруто\b",
        r"\bв натуре\b",
        r"\bпогоди\b",
        r"\bпросто\b",
        r"\bзначит\b",
        r"\bтут\b",
    ]

    def __init__(self):
        self.official_patterns = [re.compile(p, re.IGNORECASE) for p in self.official_phrases]
        self.informal_patterns = [re.compile(p, re.IGNORECASE) for p in self.informal_phrases]

    def analyze(self, text: str) -> Dict[str, Any]:
        official_count = sum(bool(p.search(text)) for p in self.official_patterns)
        informal_count = sum(bool(p.search(text)) for p in self.informal_patterns)

        tone = "официально-деловой" if official_count > informal_count else "неформальный/разговорный"

        issues = []
        if informal_count > 0:
            issues.append("Обнаружены разговорные выражения, неуместные в официальном документе.")

        result = {
            "tone": tone,
            "official_phrases_found": official_count,
            "informal_phrases_found": informal_count,
            "issues": issues,
        }
        return result


