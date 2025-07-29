from crewai_tools import BaseTool
from paddleocr import PaddleOCR, draw_ocr

class OCRTool(BaseTool):
    name = "ocr_tool"
    description = "Извлекает текст из изображения (OCR). Поддерживает JPG, PNG, PDF."

    def _run(self, image_path: str) -> str:
        # Initialize OCR with Russian and English languages
        ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

        # Perform OCR
        result = ocr.ocr(image_path, cls=True)

        # Extract text from results
        extracted_text = []
        for line in result:
            if line and isinstance(line, list):
                for item in line:
                    if isinstance(item, list) and len(item) > 1:
                        text = item[1][0]
                        extracted_text.append(text)

        return "\n".join(extracted_text)
