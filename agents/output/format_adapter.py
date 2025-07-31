









"""
Format Adapter Agent

Adapts output format to different requirements.
"""

import json
from enum import Enum
from typing import Any, Dict

class OutputFormat(str, Enum):
    """Supported output formats"""
    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"
    TEXT = "text"
    PDF = "pdf"  # Not yet implemented

class FormatAdapter:
    """
    Adapts output format to different requirements.
    """

    def __init__(self, format: OutputFormat):
        self.format = format

    def transform(self, result_object: Dict[str, Any]) -> str:
        """
        Transforms result object to specified format.

        Args:
            result_object: Result data to transform

        Returns:
            Formatted output
        """
        if self.format == OutputFormat.JSON:
            return json.dumps(result_object, indent=2, ensure_ascii=False)
        elif self.format == OutputFormat.MARKDOWN:
            return self._to_markdown(result_object)
        elif self.format == OutputFormat.HTML:
            return self._to_html(result_object)
        elif self.format == OutputFormat.TEXT:
            return self._to_text(result_object)
        elif self.format == OutputFormat.PDF:
            raise NotImplementedError("PDF format not yet supported")

    def _to_markdown(self, data: Dict[str, Any]) -> str:
        """Converts data to Markdown format"""
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"### {key}")
                for subkey, subvalue in value.items():
                    lines.append(f"- **{subkey}**: {subvalue}")
            else:
                lines.append(f"- **{key}**: {value}")
        return "\n".join(lines)

    def _to_html(self, data: Dict[str, Any]) -> str:
        """Converts data to HTML format"""
        html = ["<html><body>"]
        for key, value in data.items():
            html.append(f"<h3>{key}</h3>")
            if isinstance(value, dict):
                html.append("<ul>")
                for subkey, subvalue in value.items():
                    html.append(f"<li><strong>{subkey}</strong>: {subvalue}</li>")
                html.append("</ul>")
            else:
                html.append(f"<p>{value}</p>")
        html.append("</body></html>")
        return "\n".join(html)

    def _to_text(self, data: Dict[str, Any]) -> str:
        """Converts data to plain text format"""
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{key}:")
                for subkey, subvalue in value.items():
                    lines.append(f"  {subkey}: {subvalue}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)










