


import psutil
import time
import logging
from typing import Dict, List, Optional, Any

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseAgent

# Try to import ClickHouse client
try:
    from database.clickhouse_client import ClickHouseClient
    from config.clickhouse_config import get_clickhouse_config
    HAS_CLICKHOUSE = True
except ImportError:
    HAS_CLICKHOUSE = False
    ClickHouseClient = None

class MonitoringAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MonitoringAgent")
        self.logger = logging.getLogger("MonitoringAgent")

        # Initialize ClickHouse client
        self.clickhouse_client = None
        if HAS_CLICKHOUSE:
            try:
                config = get_clickhouse_config()
                self.clickhouse_client = ClickHouseClient(config)
                if not self.clickhouse_client.is_connected():
                    self.logger.warning("ClickHouse client not connected, metrics will not be persisted")
                    self.clickhouse_client = None
            except Exception as e:
                self.logger.error(f"Failed to initialize ClickHouse client: {e}")
                self.clickhouse_client = None

    def get_system_status(self) -> dict:
        """Get system information: CPU, RAM, uptime, etc."""
        status = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage("/")._asdict(),
            "uptime_seconds": time.time() - psutil.boot_time()
        }
        self.logger.debug(f"System status: {status}")

        # Store metrics in ClickHouse
        self._store_system_metrics(status)

        return status

    def _store_system_metrics(self, status: Dict):
        """Store system metrics in ClickHouse"""
        if not self.clickhouse_client:
            return

        try:
            # Store CPU metric
            self.clickhouse_client.store_metric(
                metric_name="system.cpu_percent",
                value=status["cpu_percent"],
                tags={"unit": "percent"},
                agent_id=self.name
            )

            # Store memory metrics
            memory = status["memory"]
            self.clickhouse_client.store_metric(
                metric_name="system.memory.used",
                value=memory["used"],
                tags={"unit": "bytes"},
                agent_id=self.name
            )
            self.clickhouse_client.store_metric(
                metric_name="system.memory.free",
                value=memory["free"],
                tags={"unit": "bytes"},
                agent_id=self.name
            )
            self.clickhouse_client.store_metric(
                metric_name="system.memory.percent",
                value=memory["percent"],
                tags={"unit": "percent"},
                agent_id=self.name
            )

            # Store disk metrics
            disk = status["disk"]
            self.clickhouse_client.store_metric(
                metric_name="system.disk.used",
                value=disk["used"],
                tags={"unit": "bytes"},
                agent_id=self.name
            )
            self.clickhouse_client.store_metric(
                metric_name="system.disk.free",
                value=disk["free"],
                tags={"unit": "bytes"},
                agent_id=self.name
            )
            self.clickhouse_client.store_metric(
                metric_name="system.disk.percent",
                value=disk["percent"],
                tags={"unit": "percent"},
                agent_id=self.name
            )

            # Store uptime
            self.clickhouse_client.store_metric(
                metric_name="system.uptime",
                value=status["uptime_seconds"],
                tags={"unit": "seconds"},
                agent_id=self.name
            )

        except Exception as e:
            self.logger.error(f"Failed to store system metrics in ClickHouse: {e}")

    def check_service_status(self) -> dict:
        """Check availability of key services (mock)."""
        # Here should be calls to ping/check external components (can be extended)
        components = {
            "LLM": self.mock_check("http://llm-host/api/health"),
            "Weaviate": self.mock_check("http://weaviate-host/v1/meta"),
            "Queue": self.mock_check("http://queue-host/status"),
        }

        # Store service status as events
        self._store_service_events(components)

        return components

    def _store_service_events(self, components: Dict):
        """Store service status as events in ClickHouse"""
        if not self.clickhouse_client:
            return

        try:
            for service, status in components.items():
                self.clickhouse_client.store_event(
                    event_type="service_status",
                    source=service,
                    details=f"Status: {status}",
                    metadata={"status": status},
                    agent_id=self.name
                )
        except Exception as e:
            self.logger.error(f"Failed to store service events in ClickHouse: {e}")

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

    def query_metrics(
        self,
        time_range: Optional[Dict[str, 'datetime']] = None,
        metric_name: Optional[str] = None,
        limit: Optional[int] = 1000
    ) -> List[Dict]:
        """
        Query metrics from ClickHouse

        Args:
            time_range: Dictionary with 'start' and 'end' datetime objects
            metric_name: Metric name to filter by
            limit: Maximum number of results to return

        Returns:
            List of metric entries
        """
        if not self.clickhouse_client:
            self.logger.warning("ClickHouse client not available, cannot query metrics")
            return []

        try:
            return self.clickhouse_client.query_metrics(
                time_range=time_range,
                metric_name=metric_name,
                limit=limit
            )
        except Exception as e:
            self.logger.error(f"Failed to query metrics from ClickHouse: {e}")
            return []

    def get_metric_aggregations(
        self,
        time_range: Optional[Dict[str, 'datetime']] = None,
        metric_name: Optional[str] = None,
        aggregation: str = 'hour'
    ) -> Dict[str, Any]:
        """
        Get metric aggregations from ClickHouse

        Args:
            time_range: Dictionary with 'start' and 'end' datetime objects
            metric_name: Metric name to filter by
            aggregation: Aggregation interval ('hour', 'day', 'minute')

        Returns:
            Dictionary with metric aggregations
        """
        if not self.clickhouse_client:
            self.logger.warning("ClickHouse client not available, cannot get metric aggregations")
            return {}

        try:
            return self.clickhouse_client.get_metric_aggregations(
                time_range=time_range,
                metric_name=metric_name,
                aggregation=aggregation
            )
        except Exception as e:
            self.logger.error(f"Failed to get metric aggregations from ClickHouse: {e}")
            return {}

