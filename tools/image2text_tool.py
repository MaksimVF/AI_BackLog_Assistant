


from crewai_tools import BaseTool
from typing import Optional
from PIL import Image
import pytesseract
import os

class ImageToTextTool(BaseTool):
    name = "image_to_text_tool"
    description = "Распознаёт текст с изображения. Поддерживает JPEG, PNG, WEBP и другие форматы."

    def _execute(self, image_path: str, lang: Optional[str] = "eng") -> str:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Файл не найден: {image_path}")

        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            return f"Ошибка при распознавании изображения: {str(e)}"


