



"""
Service Coordinator Agent - Handles continuous monitoring and system administration
"""

import sys
import json
import logging
import time
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel

# Import SuperAdminAgent for system administration
from agents.super_admin_agent import SuperAdminAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemStatus(BaseModel):
    """System status model"""
    cpu_usage: str
    memory_usage: str
    disk_space: str
    active_services: List[str]
    system_load: str
    timestamp: str

class LogAnalysis(BaseModel):
    """Log analysis model"""
    total_logs: int
    error_count: int
    warning_count: int
    critical_issues: List[str]
    recommended_actions: List[str]
    timestamp: str

class ServiceCoordinatorAgent:
    """Service Coordinator Agent for continuous monitoring and administration"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Service Coordinator Agent

        Args:
            config: Configuration options
        """
        self.config = config or {}
        self.session_id = f"service_coordinator_{int(time.time())}"
        self.running = False
        self.monitoring_thread = None
        self.system_status = None
        self.log_buffer = []
        self.alerts = []

        # Initialize SuperAdminAgent for comprehensive system administration
        self.admin = SuperAdminAgent()

        # Initialize with default status
        self._initialize_system_status()

        logger.info(f"Service Coordinator Agent initialized (Session: {self.session_id})")

    def _initialize_system_status(self):
        """Initialize system status using admin agent"""
        self.system_status = self.admin.health_check()

    def start_monitoring(self, interval: int = 60):
        """
        Start continuous system monitoring

        Args:
            interval: Monitoring interval in seconds
        """
        if self.running:
            logger.warning("Monitoring already running")
            return

        self.running = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitoring_thread.start()
        logger.info(f"Started continuous monitoring with {interval} second interval")

    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Stopped continuous monitoring")

    def _monitoring_loop(self, interval: int):
        """Main monitoring loop"""
        while self.running:
            try:
                # Update system status
                self._update_system_status()

                # Check for alerts
                self._check_alerts()

                # Sleep for interval
                time.sleep(interval)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)  # Wait before retrying

    def _update_system_status(self):
        """Update system status using admin agent"""
        # Get real system status from admin agent
        self.system_status = self.admin.health_check()
        logger.debug(f"Updated system status from admin agent")

    def _check_alerts(self):
        """Check for alert conditions"""
        system_info = self.system_status.get('system_status', {}).get('system', {})
        cpu_usage = system_info.get('cpu_percent', 0)
        memory_usage = system_info.get('memory', {}).get('percent', 0)
        disk_usage = system_info.get('disk', {}).get('percent', 0)
        disk_free = 100 - disk_usage

        # Clear previous alerts
        self.alerts = []

        # Check for critical conditions
        if cpu_usage > 90:
            self.alerts.append({
                'type': 'critical',
                'message': f"High CPU usage: {cpu_usage}%",
                'timestamp': datetime.utcnow().isoformat()
            })

        if memory_usage > 85:
            self.alerts.append({
                'type': 'critical',
                'message': f"High memory usage: {memory_usage}%",
                'timestamp': datetime.utcnow().isoformat()
            })

        if disk_free < 20:
            self.alerts.append({
                'type': 'critical',
                'message': f"Low disk space: {disk_free}% free",
                'timestamp': datetime.utcnow().isoformat()
            })

        if self.alerts:
            logger.warning(f"Alerts detected: {len(self.alerts)} critical conditions")

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return self.system_status

    def analyze_logs(self, log_data: str) -> Dict[str, Any]:
        """
        Analyze log data

        Args:
            log_data: Log data to analyze

        Returns:
            Log analysis results
        """
        # Simple log analysis
        lines = log_data.split('\n') if log_data else []
        error_count = sum(1 for line in lines if 'error' in line.lower())
        warning_count = sum(1 for line in lines if 'warning' in line.lower())

        critical_issues = []
        recommended_actions = []

        if error_count > 0:
            critical_issues.append(f"Found {error_count} error(s) in logs")
            recommended_actions.append("Investigate error sources")

        if warning_count > 3:  # More than 3 warnings is concerning
            critical_issues.append(f"Found {warning_count} warnings in logs")
            recommended_actions.append("Review warning messages")

        log_analysis = LogAnalysis(
            total_logs=len(lines),
            error_count=error_count,
            warning_count=warning_count,
            critical_issues=critical_issues,
            recommended_actions=recommended_actions,
            timestamp=datetime.utcnow().isoformat()
        )

        return log_analysis.dict()

    def get_optimization_recommendations(self, system_status: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Get resource optimization recommendations

        Args:
            system_status: Current system status (optional)

        Returns:
            List of optimization recommendations
        """
        current_status = system_status or self.get_system_status()
        system_info = current_status.get('system_status', {}).get('system', {})
        cpu_usage = int(system_info.get('cpu_percent', 0))
        memory_usage = int(system_info.get('memory', {}).get('percent', 0))

        recommendations = []

        if cpu_usage > 80:
            recommendations.append("Optimize CPU usage by balancing workload across cores")
            recommendations.append("Consider adding more CPU resources during peak hours")

        if memory_usage > 75:
            recommendations.append("Optimize memory usage by clearing unused caches")
            recommendations.append("Review memory-intensive processes")

        # General recommendations
        recommendations.append("Review and optimize long-running processes")
        recommendations.append("Consider implementing auto-scaling for high-load periods")

        return recommendations

    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get current alerts"""
        return self.alerts.copy()

    def add_log_data(self, log_data: str):
        """
        Add log data to buffer for analysis

        Args:
            log_data: Log data to add
        """
        self.log_buffer.append(log_data)
        if len(self.log_buffer) > 100:  # Limit buffer size
            self.log_buffer = self.log_buffer[-100:]

    def get_log_buffer(self) -> List[str]:
        """Get current log buffer"""
        return self.log_buffer.copy()

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status using SuperAdminAgent"""
        # Use admin agent for comprehensive status
        status = self.admin.health_check()
        return status

    def handle_exception(self, exception: Exception, source: str, context: dict = None):
        """Handle exceptions through the SuperAdminAgent"""
        return self.admin.handle_exception(exception, source, context)

    def check_access(self, user_id: str, action: str, resource: str) -> bool:
        """Check if a user has permission to perform an action"""
        return self.admin.check_access(user_id, action, resource)

    def run_security_scan(self) -> dict:
        """Run a security vulnerability scan"""
        return self.admin.run_security_scan()

    def get_admin_logs(self, level: str = None) -> list:
        """Get collected logs from SuperAdminAgent"""
        return self.admin.get_logs(level)

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_monitoring()

    def __del__(self):
        """Destructor"""
        self.stop_monitoring()

# Example usage
if __name__ == "__main__":
    print("=== Service Coordinator Agent Demo ===")

    with ServiceCoordinatorAgent() as coordinator:
        # Start monitoring
        coordinator.start_monitoring(interval=10)

        try:
            # Get initial status
            print("\n1. Initial system status:")
            status = coordinator.get_system_status()
            print(f"   CPU: {status['cpu_usage']}")
            print(f"   Memory: {status['memory_usage']}")
            print(f"   System load: {status['system_load']}")

            # Test log analysis
            print("\n2. Log analysis:")
            log_data = """[2025-08-05 10:15:30] INFO: System started
[2025-08-05 10:16:45] WARNING: High memory usage detected
[2025-08-05 10:17:22] ERROR: Connection to database failed"""

            analysis = coordinator.analyze_logs(log_data)
            print(f"   Errors: {analysis['error_count']}")
            print(f"   Warnings: {analysis['warning_count']}")
            print(f"   Critical issues: {analysis['critical_issues']}")

            # Get optimization recommendations
            print("\n3. Optimization recommendations:")
            recommendations = coordinator.get_optimization_recommendations()
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")

            # Let monitoring run for a bit
            print("\n4. Monitoring running... (press Ctrl+C to stop)")
            while True:
                time.sleep(5)
                alerts = coordinator.get_alerts()
                if alerts:
                    print(f"   🚨 Alerts detected: {len(alerts)}")
                    for alert in alerts:
                        print(f"      - {alert['message']}")

        except KeyboardInterrupt:
            print("\nStopping demo...")

    print("=== Demo completed ===")




