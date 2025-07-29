

import re
from typing import List

class TextCleaner:
    def __init__(self, lower: bool = True, remove_punctuation: bool = True, remove_multiple_spaces: bool = True):
        self.lower = lower
        self.remove_punctuation = remove_punctuation
        self.remove_multiple_spaces = remove_multiple_spaces

    def clean(self, text: str) -> str:
        """Очищает и нормализует входной текст."""
        if self.lower:
            text = text.lower()

        if self.remove_punctuation:
            # Remove punctuation but preserve apostrophes and hyphens if needed
            text = re.sub(r"[^\w\s-]", "", text)

        if self.remove_multiple_spaces:
            text = re.sub(r"\s+", " ", text)

        return text.strip()

    def clean_list(self, texts: List[str]) -> List[str]:
        """Применяет очистку к списку строк."""
        return [self.clean(t) for t in texts]

if __name__ == "__main__":
    cleaner = TextCleaner()
    raw_text = "  Это  пример! Текста,   с   пунктуацией...  "
    print(cleaner.clean(raw_text))

