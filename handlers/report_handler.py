

"""
Report Handler for processing and structuring various types of reports.

This module handles:
- Financial reports (balance sheets, income statements)
- Management reports (KPI, financial summaries)
- Operational reports
- CRM/ERP/1C exports in tabular or text format
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# Import utilities
from utils.document_classifier import DocumentClassifier
from utils.table_extractor import TableExtractor
from utils.structure_analyzer import StructureAnalyzer
from agents.analyzers.text_cleaner import TextCleaner

class ReportHandler:
    """
    Handles the processing of report documents.

    Features:
    - Report classification and parsing
    - Key financial and operational metric extraction
    - Table structure recognition
    - Preparation for embedding and storage
    """

    def __init__(self, document_path: Optional[str] = None, document_text: Optional[str] = None):
        """
        Initialize the report handler.

        Args:
            document_path: Path to the document file (optional)
            document_text: Raw text of the document (optional)
        """
        self.document_path = document_path
        self.document_text = document_text
        self.raw_text = None
        self.cleaned_text = None
        self.report_type = None
        self.tables = []
        self.metadata = {}
        self.logger = logging.getLogger(__name__)

        # Initialize utilities
        self.classifier = DocumentClassifier()
        self.table_extractor = TableExtractor()
        self.structure_analyzer = StructureAnalyzer()
        self.text_cleaner = TextCleaner()

    def load_and_prepare(self):
        """
        Load and prepare the document for processing.

        Steps:
        1. Extract text from document
        2. Clean and normalize text
        3. Classify report type
        """
        # Extract text from document (if path provided)
        if self.document_path:
            self.raw_text = self._extract_text_blocks(self.document_path)
        elif self.document_text:
            self.raw_text = self.document_text
        else:
            raise ValueError("Either document_path or document_text must be provided")

        # Clean text
        self.cleaned_text = self._clean_text(self.raw_text)

        # Classify report type
        self.report_type = self._classify_report_type(self.cleaned_text)

        self.logger.info(f"Processed report: type={self.report_type}, length={len(self.cleaned_text)}")

    def extract_structure(self):
        """
        Extract structural elements from the report.

        Steps:
        1. Extract tables
        2. Analyze report structure
        3. Extract key metrics
        """
        # Extract tables from document
        if self.document_path:
            self.tables = self._extract_tables(self.document_path)

        # Analyze report structure and extract metadata
        self.metadata = self._analyze_report_structure(self.cleaned_text, self.report_type)

        self.logger.info(f"Extracted {len(self.tables)} tables and {len(self.metadata)} metadata items")

    def format_for_embedding(self) -> Dict[str, Any]:
        """
        Format the processed report for embedding and storage.

        Returns:
            Dictionary with structured report data
        """
        return {
            "type": "report",
            "subtype": self.report_type,
            "text": self.cleaned_text,
            "tables": self.tables,
            "metadata": self.metadata,
            "source": self.document_path or "text_input",
            "timestamp": datetime.now().isoformat()
        }

    def run(self) -> Dict[str, Any]:
        """
        Run the complete report processing pipeline.

        Returns:
            Structured report data
        """
        self.load_and_prepare()
        self.extract_structure()
        return self.format_for_embedding()

    # Placeholder methods - these will be implemented as separate utilities
    def _extract_text_blocks(self, document_path: str) -> str:
        """Extract text blocks from a document file."""
        try:
            with open(document_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            return ""

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        cleaning_result = self.text_cleaner.clean(text)
        return cleaning_result.get("cleaned_text", text.strip())

    def _classify_report_type(self, text: str) -> str:
        """Classify the type of report."""
        return self.classifier.classify_report_type(text)

    def _extract_tables(self, document_path: str) -> List[Dict[str, Any]]:
        """Extract tables from a document."""
        return self.table_extractor.extract_tables_from_file(document_path)

    def _analyze_report_structure(self, text: str, report_type: str) -> Dict[str, Any]:
        """Analyze report structure and extract metadata."""
        return self.structure_analyzer.analyze_report_structure(text, report_type)

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Test with sample text
    sample_text = """
    Ежемесячный отчёт о продажах за январь 2023 года
    Общая выручка: 1 500 000 руб.
    Количество клиентов: 456
    Средний чек: 7 123 руб.
    """

    # Create and run report handler
    handler = ReportHandler(document_text=sample_text)
    result = handler.run()

    print("Report Processing Results:")
    print("=" * 50)
    print(f"Report Type: {result['subtype']}")
    print(f"Number of Tables: {len(result['tables'])}")
    print(f"Metadata: {result['metadata']}")
    print(f"Text Preview: {result['text'][:100]}...")

