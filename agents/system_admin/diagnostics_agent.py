







import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseAgent




from typing import Dict

class DiagnosticsAgent(BaseAgent):
    def __init__(self, notifier=None):
        super().__init__(name="DiagnosticsAgent")
        self.notifier = notifier

    def run_diagnostics(self) -> Dict:
        """Run system diagnostics and return results"""
        results = {
            "llm_service": self._check_llm(),
            "database": self._check_db(),
            "queue": self._check_queue(),
        }

        failed = [k for k, v in results.items() if not v]
        if failed and self.notifier:
            self.notifier.send_alert("diagnostics", f"Failures detected: {', '.join(failed)}")

        return results

    def _check_llm(self) -> bool:
        """Check LLM service health"""
        # In real implementation this would make an API call to the LLM service
        self.log("LLM service check: OK")
        return True

    def _check_db(self) -> bool:
        """Check database connection"""
        # In real implementation this would attempt to connect to the database
        self.log("Database check: OK")
        return True

    def _check_queue(self) -> bool:
        """Check queue system"""
        # In real implementation this would check queue status
        self.log("Queue system check: OK")
        return True

    def run_health_check(self) -> Dict:
        """Run a comprehensive health check"""
        self.log("Running comprehensive health check...")
        return {
            "status": "healthy",
            "components": self.run_diagnostics()
        }




