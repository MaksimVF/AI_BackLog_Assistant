









"""
Output Sanitizer Agent

Cleans and sanitizes output data.
"""

from typing import Any, Dict

class OutputSanitizer:
    """
    Cleans and sanitizes output data.
    """

    def __init__(self, compact_mode: bool = False):
        self.compact_mode = compact_mode
        self.forbidden_keys = {"_meta", "trace_id", "runtime_logs", "agent_path", "internal_id"}

    def sanitize(self, result_object: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes result object by removing sensitive or unnecessary data.

        Args:
            result_object: Result data to sanitize

        Returns:
            Sanitized data
        """
        def _clean(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {
                    k: _clean(v)
                    for k, v in obj.items()
                    if k not in self.forbidden_keys and v is not None and v != ""
                }
            elif isinstance(obj, list):
                return [_clean(item) for item in obj if item is not None]
            else:
                return obj

        cleaned = _clean(result_object)

        if self.compact_mode:
            cleaned = self._compactify(cleaned)

        return cleaned

    def _compactify(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Removes secondary blocks in compact mode.

        Args:
            data: Data to compactify

        Returns:
            Compactified data
        """
        compact_exclude = {"debug", "charts", "raw_scores"}
        return {k: v for k, v in data.items() if k not in compact_exclude}











