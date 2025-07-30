


"""
Contextual router for document processing.
Routes documents to appropriate handlers based on content analysis.
"""

from tools.text_cleaner import TextCleaner
from utils.table_extractor import TableExtractor
from utils.filetype_detector import detect_filetype
import logging

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from pathlib import Path
from typing import Optional, Dict, Any

class ContextualRouter:
    def __init__(self):
        self.routes = {
            "report": self._handle_report,
            "contract": self._handle_contract,
            "unknown": self._handle_unknown
        }
        self.table_extractor = TableExtractor()

    def route(self, file_path: str) -> Dict[str, Any]:
        """
        Route a document to the appropriate handler based on its content.

        Args:
            file_path: Path to the document file

        Returns:
            Dictionary with routing information and document data
        """
        logger.info(f"[router] Routing file: {file_path}")

        # Extract basic information
        file_type = detect_filetype(file_path)
        text_cleaner = TextCleaner()
        cleaned_text = text_cleaner.clean(open(file_path, 'r', encoding='utf-8').read())
        tables = self.table_extractor.extract_tables_from_file(file_path)

        context = {
            "file_path": file_path,
            "file_type": file_type,
            "text": cleaned_text,
            "tables": tables,
        }

        # Determine route using built-in classification
        route_key = self._determine_route(cleaned_text, tables)
        handler = self.routes.get(route_key, self._handle_unknown)
        return handler(context)

    def _determine_route(self, text: str, tables: list) -> str:
        """
        Determine the document route based on content and structure.

        Args:
            text: The text content of the document
            tables: List of tables extracted from the document

        Returns:
            Route key for handler selection
        """
        # Built-in classification logic
        text_lower = text.lower()

        report_keywords = [
            "отчёт", "отчет", "бухгалтерский баланс", "прибыль", "убытки",
            "движение денежных средств", "финансовый результат", "счета", "остатки"
        ]

        contract_keywords = [
            "договор", "стороны", "обязанности", "права", "срок действия",
            "предмет договора", "исполнитель", "заказчик", "ответственность", "реквизиты"
        ]

        if tables and any(kw in text_lower for kw in report_keywords):
            return "report"
        elif any(kw in text_lower for kw in contract_keywords):
            return "contract"
        else:
            return "unknown"

    def _handle_report(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle report documents.

        Args:
            context: Document context information

        Returns:
            Processed document data
        """
        logger.info("[router] Processing document as financial report")
        return {
            "route": "report",
            "text": context["text"],
            "tables": context["tables"],
            "meta": {
                "file_type": context["file_type"],
                "source": context["file_path"]
            }
        }

    def _handle_contract(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle contract documents.

        Args:
            context: Document context information

        Returns:
            Processed document data
        """
        logger.info("[router] Processing document as legal contract")
        return {
            "route": "contract",
            "text": context["text"],
            "tables": context["tables"],
            "meta": {
                "file_type": context["file_type"],
                "source": context["file_path"]
            }
        }

    def _handle_unknown(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle unknown document types.

        Args:
            context: Document context information

        Returns:
            Processed document data
        """
        logger.warning("[router] Document type not recognized")
        return {
            "route": "unknown",
            "text": context["text"],
            "tables": context["tables"],
            "meta": {
                "file_type": context["file_type"],
                "source": context["file_path"]
            }
        }

# Example usage
if __name__ == "__main__":
    router = ContextualRouter()
    # Test with a sample file path
    sample_path = "sample_report.pdf"
    result = router.route(sample_path)
    print(f"Routing result: {result}")

