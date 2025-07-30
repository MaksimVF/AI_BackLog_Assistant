



"""
Table extraction utilities for parsing tabular data from documents.
"""

import logging
import re
from typing import List, Dict, Any

class TableExtractor:
    """
    Extracts tables from document text.
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
        # For now, just read text and use text extraction
        # TODO: Implement PDF, Excel, etc. parsing
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.extract_tables(content)
        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            return []

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


