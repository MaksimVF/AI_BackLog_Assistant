
"""
Table parser module for extracting and structuring tabular data from text and PDF documents.
This module identifies, extracts, and structures table data from various document formats,
with support for OCR text, PDF files, and integration with advanced table extraction libraries.
"""

import re
import pandas as pd
from typing import List, Dict, Any, Optional, Union
import logging

# Set up logger
logger = logging.getLogger(__name__)

class TableParser:
    """
    Advanced table parser for extracting structured data from text and PDF documents.
    Supports multiple extraction methods and is ready for integration with ML models.
    """

    def __init__(self, min_columns: int = 3, min_rows: int = 2):
        """
        Initialize the table parser.

        Args:
            min_columns: Minimum number of columns to consider a block as a table
            min_rows: Minimum number of rows to consider a block as a table
        """
        self.min_columns = min_columns
        self.min_rows = min_rows

        # Default patterns for table detection
        self.split_pattern = r"\s{2,}|\t"  # Split by 2+ spaces or tabs
        self.header_patterns = [
            r"(?:наименование|name|description|товар|услуга)",
            r"(?:количество|qty|amount|count)",
            r"(?:цена|price|cost|стоимость)",
            r"(?:сумма|total|sum|итого)",
            r"(?:артикул|sku|code|номер)"
        ]

    def extract_tables_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract tables from plain text using regex-based detection.

        Args:
            text: Input text containing tables

        Returns:
            List of extracted tables with metadata
        """
        lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
        tables = []
        current_table = []
        in_table = False

        for i, line in enumerate(lines):
            # Check if line looks like a table row
            if len(re.findall(self.split_pattern, line)) >= self.min_columns - 1:
                if not in_table:
                    in_table = True
                    current_table = []

                row = [cell.strip() for cell in re.split(self.split_pattern, line)]
                current_table.append(row)
            else:
                if in_table:
                    # Check if we have enough rows for a valid table
                    if len(current_table) >= self.min_rows:
                        tables.append({
                            "data": current_table,
                            "start_line": i - len(current_table),
                            "end_line": i - 1,
                            "source": "text"
                        })
                    in_table = False
                    current_table = []

        # Add the last table if any
        if in_table and len(current_table) >= self.min_rows:
            tables.append({
                "data": current_table,
                "start_line": len(lines) - len(current_table),
                "end_line": len(lines) - 1,
                "source": "text"
            })

        return tables

    def detect_headers(self, table_data: List[List[str]]) -> Optional[List[str]]:
        """
        Detect header row in table data using common patterns.

        Args:
            table_data: 2D list of table cells

        Returns:
            List of header columns or None if not detected
        """
        if not table_data:
            return None

        # Check first row for header patterns
        first_row = " ".join(table_data[0]).lower()
        header_matches = 0

        for pattern in self.header_patterns:
            if re.search(pattern, first_row):
                header_matches += 1

        # If we find at least 2 header patterns, consider it a header row
        if header_matches >= 2:
            return table_data[0]
        else:
            return None

    def structure_table(self, table_data: List[List[str]]) -> Dict[str, Any]:
        """
        Structure raw table data into a more usable format.

        Args:
            table_data: 2D list of table cells

        Returns:
            Structured table with headers, rows, and metadata
        """
        structured = {
            "headers": None,
            "rows": [],
            "metadata": {
                "row_count": len(table_data),
                "column_count": len(table_data[0]) if table_data else 0,
                "has_headers": False
            }
        }

        if not table_data:
            return structured

        # Detect headers
        headers = self.detect_headers(table_data)

        if headers:
            structured["headers"] = headers
            structured["metadata"]["has_headers"] = True
            structured["rows"] = table_data[1:]  # Skip header row
        else:
            structured["rows"] = table_data

        # Update metadata
        structured["metadata"]["row_count"] = len(structured["rows"])
        if structured["rows"]:
            structured["metadata"]["column_count"] = len(structured["rows"][0])

        return structured

    def to_dataframe(self, structured_table: Dict[str, Any]) -> Optional[pd.DataFrame]:
        """
        Convert structured table to pandas DataFrame.

        Args:
            structured_table: Structured table data

        Returns:
            pandas DataFrame or None if conversion fails
        """
        try:
            if not structured_table["rows"]:
                return None

            if structured_table["headers"]:
                df = pd.DataFrame(structured_table["rows"], columns=structured_table["headers"])
            else:
                df = pd.DataFrame(structured_table["rows"])

            return df
        except Exception as e:
            logger.error(f"Error converting table to DataFrame: {e}")
            return None

    def extract_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract tables from a file (text or PDF).

        Args:
            file_path: Path to the file

        Returns:
            List of extracted tables
        """
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return self.extract_tables_from_text(text)
        elif file_path.endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_path}")
            return []

    def _extract_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract tables from PDF using text extraction.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of extracted tables
        """
        try:
            # Simple PDF text extraction (can be replaced with pdfplumber)
            import PyPDF2
            text = ""
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"

            return self.extract_tables_from_text(text)
        except ImportError:
            logger.error("PyPDF2 not installed. Install with: pip install PyPDF2")
            return []
        except Exception as e:
            logger.error(f"Error extracting tables from PDF: {e}")
            return []

    def add_custom_pattern(self, pattern: str) -> None:
        """
        Add a custom regex pattern for header detection.

        Args:
            pattern: Regex pattern to add
        """
        self.header_patterns.append(pattern)
        logger.info(f"Added custom header pattern: {pattern}")

# Example usage
if __name__ == "__main__":
    # Create parser
    parser = TableParser()

    # Sample text with table
    sample_text = """
    Наименование       Кол-во   Цена     Сумма
    Товар А            2        500.00   1000.00
    Услуга Б           1        1500.00  1500.00
    """

    # Extract tables
    tables = parser.extract_tables_from_text(sample_text)
    print(f"Found {len(tables)} tables")

    for i, table in enumerate(tables):
        print(f"\nTable {i+1}:")
        structured = parser.structure_table(table["data"])

        if structured["headers"]:
            print("Headers:", structured["headers"])

        print("Rows:")
        for row in structured["rows"]:
            print("  ", row)

        # Convert to DataFrame
        df = parser.to_dataframe(structured)
        if df is not None:
            print(f"\nDataFrame:\n{df}")

        print("-" * 50)
