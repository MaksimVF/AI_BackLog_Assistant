



"""
Table extraction utilities for parsing tabular data from documents.
"""

import os
import pdfplumber
import docx
import re
import logging
from typing import List, Dict, Any

class TableExtractor:
    """
    Extracts tables from document text and files.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_tables(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract tables from document text.

        Args:
            text: The text content of the document

        Returns:
            List of extracted tables with their structure
        """
        # Simple regex-based table extraction for now
        tables = []

        # Look for table-like structures (very basic)
        table_patterns = [
            r"(\|.*?\|.*?\|.*?\|)",  # Markdown-like tables
            r"([^\n]+\t+[^\n]+\t+[^\n]+)"  # Tab-separated values
        ]

        for pattern in table_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
            for match in matches:
                tables.append({
                    "content": match.strip(),
                    "format": "text"
                })

        self.logger.info(f"Extracted {len(tables)} tables")
        return tables

    def extract_tables_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract tables from a document file.

        Args:
            file_path: Path to the document file

        Returns:
            List of extracted tables
        """
        extension = os.path.splitext(file_path)[-1].lower()
        tables = []

        if extension == ".pdf":
            tables = self._extract_from_pdf(file_path)
        elif extension == ".docx":
            tables = self._extract_from_docx(file_path)
        elif extension in [".txt", ".csv"]:
            tables = self._extract_from_txt(file_path)
        else:
            # For other file types, try to read as text
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                tables = self.extract_tables(content)
            except Exception as e:
                self.logger.error(f"Error reading file: {e}")
                return []

        return [{"content": table, "format": "file"} for table in tables]

    def _extract_from_pdf(self, file_path: str) -> List[List[str]]:
        """
        Extract tables from PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            List of extracted tables
        """
        tables = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        cleaned = [row for row in table if any(cell for cell in row)]
                        if cleaned:
                            tables.append(cleaned)
        except Exception as e:
            self.logger.error(f"PDF extraction error: {e}")
        return tables

    def _extract_from_docx(self, file_path: str) -> List[List[str]]:
        """
        Extract tables from DOCX file.

        Args:
            file_path: Path to the DOCX file

        Returns:
            List of extracted tables
        """
        tables = []
        try:
            doc = docx.Document(file_path)
            for table in doc.tables:
                table_data = []
                for row in table.rows:
                    row_data = [cell.text.strip() for cell in row.cells]
                    table_data.append(row_data)
                if table_data:
                    tables.append(table_data)
        except Exception as e:
            self.logger.error(f"DOCX extraction error: {e}")
        return tables

    def _extract_from_txt(self, file_path: str) -> List[List[str]]:
        """
        Extract tables from TXT/CSV file.

        Args:
            file_path: Path to the TXT/CSV file

        Returns:
            List of extracted tables
        """
        tables = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if re.match(r'^(.+\t+.+)+$', line):
                        row = line.strip().split("\t")
                        tables.append([row])
        except Exception as e:
            self.logger.error(f"TXT extraction error: {e}")
        return tables

# Example usage
if __name__ == "__main__":
    extractor = TableExtractor()
    sample_text = """
    | Month   | Sales   | Expenses |
    |---------|---------|----------|
    | January | 100000  | 80000    |
    | February| 120000  | 90000    |
    """
    tables = extractor.extract_tables(sample_text)
    print(f"Found {len(tables)} tables")
    for i, table in enumerate(tables, 1):
        print(f"Table {i}: {table['content'][:50]}...")


