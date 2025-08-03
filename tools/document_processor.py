
"""
Document Processor Tool

Handles extraction of text and content from various document types:
- PDF files
- DOCX files
- TXT files
- CSV files
- Other text-based formats
"""

import mimetypes
from pathlib import Path
from typing import Union, Optional
import fitz  # PyMuPDF
import csv
import docx

class DocumentProcessor:
    """Processor for extracting content from various document types."""

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

    def detect_file_type(self) -> str:
        """Detect the file type based on extension and MIME type."""
        mime_type, _ = mimetypes.guess_type(str(self.file_path))
        suffix = self.file_path.suffix.lower()

        if mime_type:
            return f"{mime_type};{suffix}"
        else:
            return f"unknown;{suffix}"

    def extract_content(self) -> str:
        """Extract content from the document based on its file type."""
        file_type = self.detect_file_type()

        if "pdf" in file_type:
            return self._extract_pdf_content()
        elif "docx" in file_type or "word" in file_type:
            return self._extract_docx_content()
        elif "txt" in file_type or "text" in file_type:
            return self._extract_txt_content()
        elif "csv" in file_type:
            return self._extract_csv_content()
        else:
            # Default: try to read as text
            return self._extract_txt_content()

    def _extract_pdf_content(self) -> str:
        """Extract text from PDF file."""
        text = []
        with fitz.open(str(self.file_path)) as doc:
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text.append(page_text.strip())

        return "\n\n".join(text)

    def _extract_docx_content(self) -> str:
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(str(self.file_path))
            text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text.append(para.text.strip())
            return "\n\n".join(text)
        except Exception as e:
            return f"Error extracting DOCX content: {e}"

    def _extract_txt_content(self) -> str:
        """Extract text from TXT file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading text file: {e}"

    def _extract_csv_content(self) -> str:
        """Extract text from CSV file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                text = []
                for row in reader:
                    text.append(", ".join(row))
                return "\n".join(text)
        except Exception as e:
            return f"Error reading CSV file: {e}"

def extract_document_content(file_path: str) -> str:
    """Extract content from a document file."""
    processor = DocumentProcessor(file_path)
    return processor.extract_content()

def detect_document_type(file_path: str) -> str:
    """Detect the type of a document file."""
    processor = DocumentProcessor(file_path)
    return processor.detect_file_type()
