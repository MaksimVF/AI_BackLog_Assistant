







"""
Export Manager Agent

Exports data to various formats.
"""

import csv
import json
from typing import List, Dict, Any, Optional
import io

try:
    import pandas as pd
except ImportError:
    pd = None  # Excel export will be unavailable without pandas

class ExportManager:
    """
    Exports data to various formats.
    """

    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    def export(self, format: str = "json") -> Optional[bytes]:
        """
        Exports data to specified format.

        Args:
            format: Export format ('json', 'csv', 'excel')

        Returns:
            Exported data as bytes
        """
        format = format.lower()
        if format == "json":
            return self._export_json()
        elif format == "csv":
            return self._export_csv()
        elif format == "excel":
            if pd is None:
                raise ImportError("Pandas is required for Excel export. Please install with: pip install pandas xlsxwriter")
            return self._export_excel()
        else:
            raise ValueError(f"Export format '{format}' is not supported")

    def _export_json(self) -> bytes:
        """
        Exports data as JSON.

        Returns:
            JSON data as bytes
        """
        return json.dumps(self.data, ensure_ascii=False, indent=2).encode("utf-8")

    def _export_csv(self) -> bytes:
        """
        Exports data as CSV.

        Returns:
            CSV data as bytes
        """
        if not self.data:
            return b""

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.data[0].keys())
        writer.writeheader()
        writer.writerows(self.data)
        return output.getvalue().encode("utf-8")

    def _export_excel(self) -> bytes:
        """
        Exports data as Excel.

        Returns:
            Excel file as bytes
        """
        df = pd.DataFrame(self.data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()








