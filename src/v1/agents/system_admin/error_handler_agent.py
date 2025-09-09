

import traceback
from datetime import datetime
from typing import Dict, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseAgent

class ErrorHandlerAgent(BaseAgent):
    def __init__(self, log_collector=None, notifier=None):
        super().__init__(name="ErrorHandlerAgent")
        self.log_collector = log_collector
        self.notifier = notifier

    def handle_exception(self, exception: Exception, source: str, context: Optional[Dict] = None) -> Dict:
        """Handle an exception and return information about it"""
        error_details = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
            "exception_type": type(exception).__name__,
            "message": str(exception),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }

        if self.log_collector:
            self.log_collector.collect_log(
                source=source,
                level="ERROR",
                message=f"{type(exception).__name__}: {str(exception)}",
                context=error_details
            )

        if self.notifier:
            self.notifier.send_alert("error", f"Error in {source}: {str(exception)}")

        self._handle_logic(error_details)
        return error_details

    def _handle_logic(self, error_details: Dict):
        """For now just log, but can be extended with recovery mechanisms"""
        self.log(f"Handled error: {error_details['message']}")

    def suggest_recovery(self, error_type: str, context: Dict = None) -> str:
        recovery_actions = {
            "ConnectionError": "Check server or database connection.",
            "TimeoutError": "Try the operation again later.",
            "ValueError": "Verify input data correctness.",
            "FileNotFoundError": "Ensure the file exists and path is correct.",
            "KeyError": "Check all required keys are present in the dictionary.",
        }
        return recovery_actions.get(error_type, "Contact system administrator.")

