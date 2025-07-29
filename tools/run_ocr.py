# tools/run_ocr.py

from crewai_tools import BaseTool

class RunOCRTool(BaseTool):
    name = "run_ocr"
    description = "Выполняет OCR на изображениях для извлечения текста"

    def _run(self, image_file_path: str) -> str:
        # TODO: Implement using easyocr, tesseract or paddleocr
        return "Реализация будет добавлена позже"
