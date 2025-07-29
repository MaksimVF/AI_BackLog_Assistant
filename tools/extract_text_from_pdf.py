# tools/extract_text_from_pdf.py

from crewai_tools import BaseTool

class ExtractTextFromPDFTool(BaseTool):
    name = "extract_text_from_pdf"
    description = "Извлекает текст из PDF файла"

    def _run(self, pdf_file_path: str) -> str:
        # TODO: Implement using PyMuPDF, pdfplumber or similar
        return "Реализация будет добавлена позже"
