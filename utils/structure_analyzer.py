




"""
Report structure analysis utilities for extracting metadata and key metrics.
"""

import logging
import re
from typing import Dict, Any

class StructureAnalyzer:
    """
    Analyzes report structure and extracts key information.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_report_structure(self, text: str, report_type: str) -> Dict[str, Any]:
        """
        Analyze report structure and extract metadata.

        Args:
            text: The text content of the report
            report_type: The type of report

        Returns:
            Dictionary with extracted metadata
        """
        metadata = {
            "period": self._extract_period(text),
            "currency": self._extract_currency(text),
            "key_metrics": self._extract_key_metrics(text, report_type)
        }

        self.logger.info(f"Extracted metadata: {metadata}")
        return metadata

    def _extract_period(self, text: str) -> str:
        """Extract reporting period from text."""
        # Look for date patterns
        date_patterns = [
            r"\b(январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь)[\s,]\s?\d{4}\b",
            r"\b\d{2}\.\d{2}\.\d{4}\b",
            r"\b\d{4}\s?года\b"
        ]

        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return ", ".join(matches)

        return "unknown"

    def _extract_currency(self, text: str) -> str:
        """Extract currency information."""
        currency_patterns = [
            r"\b(руб|рублей|рубля|USD|EUR|₽|\$|€)\b"
        ]

        for pattern in currency_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].upper()

        return "unknown"

    def _extract_key_metrics(self, text: str, report_type: str) -> Dict[str, Any]:
        """Extract key metrics based on report type."""
        metrics = {}

        if report_type in ["financial", "sales"]:
            # Extract financial metrics
            metrics.update(self._extract_financial_metrics(text))
        elif report_type == "operational":
            # Extract operational metrics
            metrics.update(self._extract_operational_metrics(text))

        return metrics

    def _extract_financial_metrics(self, text: str) -> Dict[str, float]:
        """Extract financial metrics from text."""
        metrics = {}

        # Look for revenue patterns
        revenue_patterns = [
            r"выручка[\s:]+([\d\s,]+)",
            r"общая[\s]+выручка[\s:]+([\d\s,]+)",
            r"доход[\s:]+([\d\s,]+)"
        ]

        for pattern in revenue_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Clean and convert to float
                revenue_str = matches[0].replace(" ", "").replace(",", ".")
                try:
                    metrics["revenue"] = float(revenue_str)
                except ValueError:
                    pass
                break

        return metrics

    def _extract_operational_metrics(self, text: str) -> Dict[str, float]:
        """Extract operational metrics from text."""
        metrics = {}

        # Look for KPI patterns
        kpi_patterns = [
            r"KPI[\s:]+([\d\.]+)",
            r"эффективность[\s:]+([\d\.]+)%"
        ]

        for pattern in kpi_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    metrics["kpi"] = float(matches[0])
                except ValueError:
                    pass

        return metrics

# Example usage
if __name__ == "__main__":
    analyzer = StructureAnalyzer()
    sample_text = """
    Ежемесячный отчёт о продажах за январь 2023 года
    Общая выручка: 1 500 000 руб.
    Количество клиентов: 456
    Средний чек: 7 123 руб.
    """
    metadata = analyzer.analyze_report_structure(sample_text, "sales")
    print(f"Extracted metadata: {metadata}")


