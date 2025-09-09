

"""
Service Coordinator Agent - Enhanced version with comprehensive system monitoring and real metrics
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
    """Enhanced system status model with comprehensive metrics"""
    cpu_usage: str
    memory_usage: str
    disk_space: str
    active_services: List[str]
    system_load: str
    timestamp: str

class LogAnalysis(BaseModel):
    """Enhanced log analysis model with pattern detection"""
    total_logs: int
    error_count: int
    warning_count: int
    critical_count: int = 0
    info_count: int = 0
    error_patterns: Dict[str, int] = {}
    warning_patterns: Dict[str, int] = {}
    critical_issues: List[str]
    recommended_actions: List[str]
    timestamp: str

class ServiceCoordinatorAgent:
    """Enhanced Service Coordinator Agent for comprehensive monitoring and administration"""

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

        logger.info(f"Enhanced Service Coordinator Agent initialized (Session: {self.session_id})")

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
        """Check for alert conditions with comprehensive thresholds"""
        # Get comprehensive system status
        system_status = self.system_status.get('system_status', {})
        system_info = system_status.get('system', {})

        # Extract metrics with fallback defaults
        cpu_info = system_info.get('cpu', {})
        cpu_usage = cpu_info.get('percent', 0)
        cpu_load_avg = cpu_info.get('load_avg', {})

        memory_info = system_info.get('memory', {})
        virtual_memory = memory_info.get('virtual', {})
        memory_usage = virtual_memory.get('percent', 0)

        disk_info = system_info.get('disk', {})
        disk_usage = disk_info.get('usage', {}).get('percent', 0)
        disk_free = 100 - disk_usage

        processes_info = system_info.get('processes', {})
        process_count = processes_info.get('count', 0)

        # Clear previous alerts
        self.alerts = []

        # Check for critical conditions with more sophisticated thresholds
        if cpu_usage > 90:
            self.alerts.append({
                'type': 'critical',
                'message': f"High CPU usage: {cpu_usage}%",
                'recommendation': 'Consider adding more CPU resources or optimizing processes',
                'timestamp': datetime.utcnow().isoformat()
            })
        elif cpu_usage > 80:
            self.alerts.append({
                'type': 'warning',
                'message': f"Elevated CPU usage: {cpu_usage}%",
                'recommendation': 'Monitor CPU usage closely',
                'timestamp': datetime.utcnow().isoformat()
            })

        # Check CPU load average
        if cpu_load_avg.get('15_min', 0) > cpu_info.get('logical_cores', 1) * 0.8:
            self.alerts.append({
                'type': 'warning',
                'message': f"High CPU load average (15min): {cpu_load_avg.get('15_min'):.2f}",
                'recommendation': 'Investigate long-running processes',
                'timestamp': datetime.utcnow().isoformat()
            })

        # Memory alerts
        if memory_usage > 90:
            self.alerts.append({
                'type': 'critical',
                'message': f"High memory usage: {memory_usage}%",
                'recommendation': 'Consider adding more RAM or optimizing memory usage',
                'timestamp': datetime.utcnow().isoformat()
            })
        elif memory_usage > 80:
            self.alerts.append({
                'type': 'warning',
                'message': f"Elevated memory usage: {memory_usage}%",
                'recommendation': 'Monitor memory usage closely',
                'timestamp': datetime.utcnow().isoformat()
            })

        # Disk alerts
        if disk_free < 10:
            self.alerts.append({
                'type': 'critical',
                'message': f"Critical low disk space: {disk_free}% free",
                'recommendation': 'Immediately free up disk space',
                'timestamp': datetime.utcnow().isoformat()
            })
        elif disk_free < 20:
            self.alerts.append({
                'type': 'warning',
                'message': f"Low disk space: {disk_free}% free",
                'recommendation': 'Plan to free up disk space soon',
                'timestamp': datetime.utcnow().isoformat()
            })

        # Process count alerts
        if process_count > 500:  # Threshold for high process count
            self.alerts.append({
                'type': 'warning',
                'message': f"High process count: {process_count}",
                'recommendation': 'Investigate potential process leaks',
                'timestamp': datetime.utcnow().isoformat()
            })

        # Check service status alerts
        services_status = system_status.get('services', {})
        for service, status in services_status.items():
            if status != 'ok':
                self.alerts.append({
                    'type': 'critical',
                    'message': f"Service {service} is down or unreachable",
                    'recommendation': f'Check {service} service status',
                    'timestamp': datetime.utcnow().isoformat()
                })

        if self.alerts:
            logger.warning(f"Alerts detected: {len(self.alerts)} conditions requiring attention")

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return self.system_status

    def analyze_logs(self, log_data: str) -> Dict[str, Any]:
        """
        Analyze log data with enhanced pattern recognition

        Args:
            log_data: Log data to analyze

        Returns:
            Log analysis results with detailed insights
        """
        # Enhanced log analysis
        lines = log_data.split('\n') if log_data else []

        # Count different log levels
        error_count = 0
        warning_count = 0
        info_count = 0
        critical_count = 0

        # Track specific error patterns
        error_patterns = {}
        warning_patterns = {}

        # Common patterns to detect
        patterns_to_detect = {
            'database': ['database', 'db connection', 'sql error', 'connection failed'],
            'memory': ['memory leak', 'out of memory', 'memory error'],
            'network': ['network error', 'connection timeout', 'socket error'],
            'performance': ['slow query', 'high latency', 'timeout'],
            'security': ['unauthorized', 'access denied', 'security violation']
        }

        for line in lines:
            lower_line = line.lower()

            if 'error' in lower_line or 'exception' in lower_line or 'critical' in lower_line:
                error_count += 1
                if 'critical' in lower_line:
                    critical_count += 1

                # Check for specific patterns
                for pattern_type, keywords in patterns_to_detect.items():
                    if any(keyword in lower_line for keyword in keywords):
                        error_patterns[pattern_type] = error_patterns.get(pattern_type, 0) + 1

            elif 'warning' in lower_line or 'warn' in lower_line:
                warning_count += 1
                for pattern_type, keywords in patterns_to_detect.items():
                    if any(keyword in lower_line for keyword in keywords):
                        warning_patterns[pattern_type] = warning_patterns.get(pattern_type, 0) + 1

            elif 'info' in lower_line or 'information' in lower_line:
                info_count += 1

        # Generate critical issues and recommendations
        critical_issues = []
        recommended_actions = []

        # General issues
        if error_count > 0:
            critical_issues.append(f"Found {error_count} error(s) in logs")
            recommended_actions.append("Investigate error sources immediately")

        if critical_count > 0:
            critical_issues.append(f"Found {critical_count} critical error(s)")
            recommended_actions.append("Address critical errors urgently")

        if warning_count > 5:  # More than 5 warnings is concerning
            critical_issues.append(f"Found {warning_count} warnings in logs")
            recommended_actions.append("Review warning messages")

        # Specific pattern issues
        for pattern_type, count in error_patterns.items():
            if count > 0:
                critical_issues.append(f"Found {count} {pattern_type}-related error(s)")
                if pattern_type == 'database':
                    recommended_actions.append("Check database connections and queries")
                elif pattern_type == 'memory':
                    recommended_actions.append("Investigate memory usage and leaks")
                elif pattern_type == 'network':
                    recommended_actions.append("Check network connectivity and configurations")
                elif pattern_type == 'performance':
                    recommended_actions.append("Optimize slow operations and queries")
                elif pattern_type == 'security':
                    recommended_actions.append("Review security configurations immediately")

        # Add general recommendations based on log volume
        if len(lines) > 1000:
            recommended_actions.append("Consider implementing log rotation")
        if error_count > 10:
            recommended_actions.append("Enable detailed error logging for debugging")
        if warning_count > 20:
            recommended_actions.append("Review application configurations")

        log_analysis = LogAnalysis(
            total_logs=len(lines),
            error_count=error_count,
            warning_count=warning_count,
            critical_count=critical_count,
            info_count=info_count,
            error_patterns=error_patterns,
            warning_patterns=warning_patterns,
            critical_issues=critical_issues,
            recommended_actions=recommended_actions,
            timestamp=datetime.utcnow().isoformat()
        )

        return log_analysis.dict()

    def get_optimization_recommendations(self, system_status: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Get comprehensive resource optimization recommendations based on detailed system metrics

        Args:
            system_status: Current system status (optional)

        Returns:
            List of optimization recommendations with specific actions
        """
        current_status = system_status or self.get_system_status()
        system_info = current_status.get('system_status', {}).get('system', {})

        # Extract detailed metrics
        cpu_info = system_info.get('cpu', {})
        cpu_usage = cpu_info.get('percent', 0)
        cpu_cores = cpu_info.get('logical_cores', 1)
        cpu_load_avg = cpu_info.get('load_avg', {})

        memory_info = system_info.get('memory', {})
        virtual_memory = memory_info.get('virtual', {})
        memory_usage = virtual_memory.get('percent', 0)
        memory_used = virtual_memory.get('used', 0)
        memory_total = virtual_memory.get('total', 1)

        disk_info = system_info.get('disk', {})
        disk_usage = disk_info.get('usage', {}).get('percent', 0)
        disk_used = disk_info.get('usage', {}).get('used', 0)
        disk_total = disk_info.get('usage', {}).get('total', 1)

        process_info = system_info.get('processes', {})
        process_count = process_info.get('count', 0)
        top_processes = process_info.get('top_processes', [])

        recommendations = []

        # CPU optimization recommendations
        if cpu_usage > 90:
            recommendations.append("🚨 CRITICAL: CPU usage > 90% - Immediate action required")
            recommendations.append("  - Identify and terminate unnecessary processes")
            recommendations.append("  - Consider emergency scaling or load balancing")
        elif cpu_usage > 80:
            recommendations.append("⚠️  WARNING: CPU usage > 80% - Optimize workload")
            recommendations.append("  - Review and optimize CPU-intensive processes")
            recommendations.append("  - Implement process prioritization")

        # CPU load average analysis
        if cpu_load_avg.get('15_min', 0) > cpu_cores:
            recommendations.append(f"⚠️  High CPU load average (15min): {cpu_load_avg.get('15_min'):.2f}")
            recommendations.append("  - Investigate long-running or blocked processes")
            recommendations.append("  - Consider adding more CPU cores")

        # Memory optimization recommendations
        if memory_usage > 90:
            recommendations.append("🚨 CRITICAL: Memory usage > 90% - Immediate action required")
            recommendations.append("  - Restart memory-intensive services")
            recommendations.append("  - Add more RAM immediately")
        elif memory_usage > 80:
            recommendations.append("⚠️  WARNING: Memory usage > 80% - Optimize memory usage")
            recommendations.append("  - Clear unused caches and temporary data")
            recommendations.append("  - Optimize memory allocation in applications")

        # Check for memory leaks
        if memory_used > 0.9 * memory_total and process_count > 100:
            recommendations.append("⚠️  Potential memory leak detected")
            recommendations.append("  - Monitor memory usage over time")
            recommendations.append("  - Identify processes with growing memory usage")

        # Disk optimization recommendations
        if disk_usage > 90:
            recommendations.append("🚨 CRITICAL: Disk usage > 90% - Immediate action required")
            recommendations.append("  - Delete unnecessary files and logs")
            recommendations.append("  - Add more storage capacity immediately")
        elif disk_usage > 80:
            recommendations.append("⚠️  WARNING: Disk usage > 80% - Free up space")
            recommendations.append("  - Implement log rotation and cleanup policies")
            recommendations.append("  - Archive old data to external storage")

        # Process optimization recommendations
        if process_count > 500:
            recommendations.append("⚠️  High process count detected")
            recommendations.append("  - Investigate potential process leaks")
            recommendations.append("  - Review process management policies")

        # Top process analysis
        if top_processes:
            high_cpu_processes = [p for p in top_processes if p.get('cpu_percent', 0) > 50]
            high_memory_processes = [p for p in top_processes if p.get('memory_percent', 0) > 30]

            if high_cpu_processes:
                recommendations.append("⚠️  Processes with high CPU usage:")
                for proc in high_cpu_processes:
                    recommendations.append(f"  - {proc.get('name')}: {proc.get('cpu_percent')}% CPU")

            if high_memory_processes:
                recommendations.append("⚠️  Processes with high memory usage:")
                for proc in high_memory_processes:
                    recommendations.append(f"  - {proc.get('name')}: {proc.get('memory_percent')}% memory")

        # General best practices
        recommendations.append("\n🔧 General optimization recommendations:")
        recommendations.append("  - Implement auto-scaling for peak load periods")
        recommendations.append("  - Set up regular system maintenance windows")
        recommendations.append("  - Monitor system metrics continuously")
        recommendations.append("  - Implement resource quotas and limits")

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
    print("=== Enhanced Service Coordinator Agent Demo ===")

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
            print("\n2. Enhanced log analysis:")
            log_data = """[2025-08-05 10:15:30] INFO: System started
[2025-08-05 10:16:45] WARNING: High memory usage detected
[2025-08-05 10:17:22] ERROR: Connection to database failed
[2025-08-05 10:18:10] ERROR: Memory leak detected in process 1234
[2025-08-05 10:19:05] CRITICAL: System unresponsive due to high load"""

            analysis = coordinator.analyze_logs(log_data)
            print(f"   Errors: {analysis['error_count']}")
            print(f"   Warnings: {analysis['warning_count']}")
            print(f"   Critical issues: {analysis['critical_issues']}")
            print(f"   Recommendations: {analysis['recommended_actions']}")

            # Get optimization recommendations
            print("\n3. Comprehensive optimization recommendations:")
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

