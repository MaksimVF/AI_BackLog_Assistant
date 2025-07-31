








"""
Output Dispatcher Agent

Handles delivery of final results to appropriate interfaces.
"""

import json
from enum import Enum
from typing import Any, Dict, Union

class OutputMode(str, Enum):
    """Output delivery modes"""
    UI = "ui"
    API = "api"
    FILE = "file"
    EXTERNAL = "external"

class OutputDispatcher:
    """
    Handles delivery of final results to appropriate interfaces.
    """

    def __init__(self, mode: OutputMode):
        self.mode = mode

    def dispatch(self, formatted_response: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Dispatches formatted response to appropriate interface.

        Args:
            formatted_response: Formatted response data

        Returns:
            Dispatch result
        """
        if self.mode == OutputMode.UI:
            return self._to_ui(formatted_response)
        elif self.mode == OutputMode.API:
            return self._to_api(formatted_response)
        elif self.mode == OutputMode.FILE:
            return self._to_file(formatted_response)
        elif self.mode == OutputMode.EXTERNAL:
            return self._to_external(formatted_response)
        else:
            raise ValueError(f"Unknown output mode: {self.mode}")

    def _to_ui(self, data: Dict[str, Any]) -> str:
        """Formats output for UI display"""
        return f"[UI Rendered Output]: {data.get('summary', 'No data available')}"

    def _to_api(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats output for API response"""
        return {
            "status": "ok",
            "data": data,
            "meta": {"dispatched_by": "OutputDispatcher"}
        }

    def _to_file(self, data: Dict[str, Any]) -> str:
        """Saves output to file"""
        filename = f"output_{data.get('task_id', 'unknown')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return f"File saved as {filename}"

    def _to_external(self, data: Dict[str, Any]) -> str:
        """Handles external system integration"""
        return "External system integration not yet implemented"









