




"""
Table Renderer Agent

Generates table representations of data.
"""

import csv
import io
from typing import List, Dict, Any, Optional

class TableRenderer:
    """
    Renders data as HTML tables and exports to CSV.
    """

    def __init__(self, data: List[Dict[str, Any]], headers: Optional[List[str]] = None):
        """
        Args:
            data: List of dictionaries where each dictionary is a table row
            headers: List of column headers. If None, uses keys from first dictionary.
        """
        if not data:
            raise ValueError("Data cannot be empty")

        self.data = data
        self.headers = headers or list(data[0].keys())

    def render_html(self) -> str:
        """
        Renders data as HTML table.

        Returns:
            HTML string
        """
        html = ['<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse; font-family: Arial, sans-serif;">']
        # Table header
        html.append("<thead><tr style='background-color: #f2f2f2;'>")
        for header in self.headers:
            html.append(f"<th style='padding: 8px; text-align: left;'>{header}</th>")
        html.append("</tr></thead>")

        # Table body
        html.append("<tbody>")
        for row in self.data:
            html.append("<tr>")
            for header in self.headers:
                cell = str(row.get(header, ""))
                html.append(f"<td style='padding: 8px;'>{cell}</td>")
            html.append("</tr>")
        html.append("</tbody></table>")
        return "".join(html)

    def export_csv(self) -> str:
        """
        Exports data as CSV.

        Returns:
            CSV string
        """
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.headers)
        writer.writeheader()
        # Filter data to only include specified headers
        filtered_data = []
        for row in self.data:
            filtered_row = {key: row.get(key, "") for key in self.headers}
            filtered_data.append(filtered_row)
        writer.writerows(filtered_data)
        return output.getvalue()

    def export_excel(self) -> bytes:
        """
        Exports data as Excel (requires pandas).

        Returns:
            Excel file as bytes
        """
        try:
            import pandas as pd
            df = pd.DataFrame(self.data)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()
        except ImportError:
            raise ImportError("Pandas is required for Excel export. Please install with: pip install pandas xlsxwriter")






