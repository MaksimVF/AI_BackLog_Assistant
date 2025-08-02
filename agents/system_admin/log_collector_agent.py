

import logging
from datetime import datetime
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseAgent

class LogCollectorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="LogCollectorAgent")
        self.collected_logs: List[Dict] = []
        self.logger = logging.getLogger("LogCollectorAgent")

    def collect_log(self, source: str, level: str, message: str, context: Dict = None):
        """Collect a log from a given source"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
            "level": level.upper(),
            "message": message,
            "context": context or {}
        }
        self.collected_logs.append(log_entry)
        self.logger.debug(f"Log collected: {log_entry}")

    def filter_logs(self, level: str = "ERROR") -> List[Dict]:
        """Filter logs by level"""
        return [log for log in self.collected_logs if log["level"] == level.upper()]

    def export_logs(self) -> List[Dict]:
        """Return all collected logs"""
        return self.collected_logs

    def clear_logs(self):
        """Clear all logs (e.g., at the end of a monitoring session)"""
        self.logger.debug("Logs cleared.")
        self.collected_logs.clear()

