


# tools/pdf_extractor.py

from pathlib import Path
from typing import Union, List
import fitz  # PyMuPDF

class PDFExtractor:
    def __init__(self, filepath: Union[str, Path]):
        self.filepath = Path(filepath)

    def extract_text(self) -> str:
        """Извлекает текст из PDF-файла постранично."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"Файл не найден: {self.filepath}")

        text = []
        with fitz.open(str(self.filepath)) as doc:
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text.append(page_text.strip())

        return "\n\n".join(text)

    def extract_text_by_pages(self) -> List[str]:
        """Возвращает список текстов по страницам (для анализа структуры)."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"Файл не найден: {self.filepath}")

        pages = []
        with fitz.open(str(self.filepath)) as doc:
            for page in doc:
                pages.append(page.get_text().strip())

        return pages

def extract_text_from_pdf(pdf_file_path: str) -> str:
    """Функция для извлечения текста из PDF файла."""
    extractor = PDFExtractor(pdf_file_path)
    return extractor.extract_text()

if __name__ == "__main__":
    # Пример использования
    extractor = PDFExtractor("sample_invoice.pdf")
    full_text = extractor.extract_text()
    print(full_text)

