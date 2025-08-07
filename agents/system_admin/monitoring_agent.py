


import psutil
import time
import logging
import sys
from datetime import datetime
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
        """Get comprehensive system information including CPU, RAM, disk, network, and process metrics."""
        # Get basic system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_times = psutil.cpu_times_percent(interval=1)
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage("/")
        disk_io = psutil.disk_io_counters()
        net_io = psutil.net_io_counters()
        boot_time = datetime.fromtimestamp(psutil.boot_time()).isoformat()
        uptime_seconds = time.time() - psutil.boot_time()

        # Get process information
        process_count = len(psutil.pids())
        top_processes = self._get_top_processes(limit=5)

        # Get system load average
        load_avg = psutil.getloadavg()

        status = {
            "cpu": {
                "percent": cpu_percent,
                "times_percent": cpu_times._asdict(),
                "logical_cores": psutil.cpu_count(logical=True),
                "physical_cores": psutil.cpu_count(logical=False),
                "load_avg": {
                    "1_min": load_avg[0],
                    "5_min": load_avg[1],
                    "15_min": load_avg[2]
                }
            },
            "memory": {
                "virtual": memory._asdict(),
                "swap": swap._asdict()
            },
            "disk": {
                "usage": disk._asdict(),
                "io_counters": disk_io._asdict()
            },
            "network": {
                "io_counters": net_io._asdict()
            },
            "processes": {
                "count": process_count,
                "top_processes": top_processes
            },
            "system": {
                "uptime_seconds": uptime_seconds,
                "boot_time": boot_time,
                "platform": sys.platform,
                "python_version": sys.version.split()[0]
            }
        }

        self.logger.debug(f"Comprehensive system status collected")

        # Store metrics in ClickHouse
        self._store_system_metrics(status)

        return status

    def _store_system_metrics(self, status: Dict):
        """Store comprehensive system metrics in ClickHouse"""
        if not self.clickhouse_client:
            return

        try:
            # Store CPU metrics
            cpu = status["cpu"]
            self.clickhouse_client.store_metric(
                metric_name="system.cpu_percent",
                value=cpu["percent"],
                tags={"unit": "percent"},
                agent_id=self.name
            )

            # Store CPU times
            for cpu_type, value in cpu["times_percent"].items():
                self.clickhouse_client.store_metric(
                    metric_name=f"system.cpu_{cpu_type}",
                    value=value,
                    tags={"unit": "percent"},
                    agent_id=self.name
                )

            # Store memory metrics
            memory = status["memory"]["virtual"]
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

            # Store swap memory metrics
            swap = status["memory"]["swap"]
            self.clickhouse_client.store_metric(
                metric_name="system.swap.used",
                value=swap["used"],
                tags={"unit": "bytes"},
                agent_id=self.name
            )
            self.clickhouse_client.store_metric(
                metric_name="system.swap.free",
                value=swap["free"],
                tags={"unit": "bytes"},
                agent_id=self.name
            )
            self.clickhouse_client.store_metric(
                metric_name="system.swap.percent",
                value=swap["percent"],
                tags={"unit": "percent"},
                agent_id=self.name
            )

            # Store disk metrics
            disk = status["disk"]["usage"]
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

            # Store disk IO metrics
            disk_io = status["disk"]["io_counters"]
            self.clickhouse_client.store_metric(
                metric_name="system.disk.io.read_bytes",
                value=disk_io["read_bytes"],
                tags={"unit": "bytes"},
                agent_id=self.name
            )
            self.clickhouse_client.store_metric(
                metric_name="system.disk.io.write_bytes",
                value=disk_io["write_bytes"],
                tags={"unit": "bytes"},
                agent_id=self.name
            )

            # Store network metrics
            net_io = status["network"]["io_counters"]
            self.clickhouse_client.store_metric(
                metric_name="system.network.bytes_sent",
                value=net_io["bytes_sent"],
                tags={"unit": "bytes"},
                agent_id=self.name
            )
            self.clickhouse_client.store_metric(
                metric_name="system.network.bytes_recv",
                value=net_io["bytes_recv"],
                tags={"unit": "bytes"},
                agent_id=self.name
            )

            # Store process metrics
            self.clickhouse_client.store_metric(
                metric_name="system.processes.count",
                value=status["processes"]["count"],
                tags={"unit": "count"},
                agent_id=self.name
            )

            # Store system metrics
            system = status["system"]
            self.clickhouse_client.store_metric(
                metric_name="system.uptime",
                value=system["uptime_seconds"],
                tags={"unit": "seconds"},
                agent_id=self.name
            )

            # Store CPU load average
            load_avg = cpu["load_avg"]
            self.clickhouse_client.store_metric(
                metric_name="system.cpu.load_avg.1min",
                value=load_avg["1_min"],
                tags={"unit": "load"},
                agent_id=self.name
            )
            self.clickhouse_client.store_metric(
                metric_name="system.cpu.load_avg.5min",
                value=load_avg["5_min"],
                tags={"unit": "load"},
                agent_id=self.name
            )
            self.clickhouse_client.store_metric(
                metric_name="system.cpu.load_avg.15min",
                value=load_avg["15_min"],
                tags={"unit": "load"},
                agent_id=self.name
            )

        except Exception as e:
            self.logger.error(f"Failed to store system metrics in ClickHouse: {e}")

    def _get_top_processes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top processes by memory and CPU usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'user': proc.info['username'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_percent': proc.info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Sort by CPU and memory usage
            processes.sort(key=lambda x: (x['cpu_percent'], x['memory_percent']), reverse=True)

            return processes[:limit]
        except Exception as e:
            self.logger.error(f"Error getting top processes: {e}")
            return []

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

    def check_specific_process(self, process_name: str) -> Dict[str, Any]:
        """Check if a specific process is running."""
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name.lower() in proc.info['name'].lower():
                return {
                    "status": "running",
                    "pid": proc.info['pid'],
                    "name": proc.info['name']
                }

        return {
            "status": "not_found",
            "process_name": process_name
        }

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

