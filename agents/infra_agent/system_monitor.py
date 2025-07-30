




import psutil
from typing import Dict, Any, Optional
from .base_infra_agent import BaseInfraAgent

class SystemMonitorAgent(BaseInfraAgent):
    """Agent to monitor system resources."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        config = config or {}
        super().__init__(
            name="SystemMonitor",
            config={
                "cpu_threshold": config.get("cpu_threshold", 80.0),
                "memory_threshold": config.get("memory_threshold", 80.0),
                "disk_threshold": config.get("disk_threshold", 80.0)
            }
        )

    def check_status(self) -> Dict[str, Any]:
        """Check system resource usage."""
        # CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_status = "normal" if cpu_usage < self.config["cpu_threshold"] else "high"

        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        memory_status = "normal" if memory_usage < self.config["memory_threshold"] else "high"

        # Disk usage
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        disk_status = "normal" if disk_usage < self.config["disk_threshold"] else "high"

        # Determine overall status
        overall_status = "normal"
        if cpu_status == "high" or memory_status == "high" or disk_status == "high":
            overall_status = "high_load"

        return {
            "status": overall_status,
            "cpu": {
                "usage_percent": cpu_usage,
                "status": cpu_status,
                "cores": psutil.cpu_count(logical=True)
            },
            "memory": {
                "usage_percent": memory_usage,
                "status": memory_status,
                "total": f"{memory.total / (1024**3):.2f} GB",
                "available": f"{memory.available / (1024**3):.2f} GB"
            },
            "disk": {
                "usage_percent": disk_usage,
                "status": disk_status,
                "total": f"{disk.total / (1024**3):.2f} GB",
                "free": f"{disk.free / (1024**3):.2f} GB"
            }
        }

    def get_detailed_stats(self) -> Dict[str, Any]:
        """Get detailed system statistics."""
        # Network stats
        net_io = psutil.net_io_counters()
        net_status = {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }

        # Disk I/O stats
        disk_io = psutil.disk_io_counters()
        disk_io_status = {
            "read_count": disk_io.read_count,
            "write_count": disk_io.write_count,
            "read_bytes": disk_io.read_bytes,
            "write_bytes": disk_io.write_bytes
        }

        # Process count
        process_count = len(psutil.pids())

        return {
            "network": net_status,
            "disk_io": disk_io_status,
            "processes": process_count,
            "uptime": psutil.boot_time()
        }

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



