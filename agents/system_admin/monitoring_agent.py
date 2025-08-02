


import psutil
import time
import logging

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseAgent


class MonitoringAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MonitoringAgent")
        self.logger = logging.getLogger("MonitoringAgent")

    def get_system_status(self) -> dict:
        """Get system information: CPU, RAM, uptime, etc."""
        status = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage("/")._asdict(),
            "uptime_seconds": time.time() - psutil.boot_time()
        }
        self.logger.debug(f"System status: {status}")
        return status

    def check_service_status(self) -> dict:
        """Check availability of key services (mock)."""
        # Here should be calls to ping/check external components (can be extended)
        components = {
            "LLM": self.mock_check("http://llm-host/api/health"),
            "Weaviate": self.mock_check("http://weaviate-host/v1/meta"),
            "Queue": self.mock_check("http://queue-host/status"),
        }
        return components

    def mock_check(self, url: str) -> str:
        # In real implementation there should be `requests.get(url)` or ping
        self.logger.debug(f"Checking component: {url}")
        return "ok"  # or "unreachable"

    def report(self) -> dict:
        """Generate a final system status report."""
        return {
            "system": self.get_system_status(),
            "services": self.check_service_status()
        }


