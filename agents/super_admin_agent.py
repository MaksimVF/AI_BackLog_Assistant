


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base import BaseAgent
from system_admin.error_handler_agent import ErrorHandlerAgent
from system_admin.log_collector_agent import LogCollectorAgent
from system_admin.notification_agent import NotificationAgent
from system_admin.security_agent import SecurityAgent
from system_admin.diagnostics_agent import DiagnosticsAgent
from system_admin.monitoring_agent import MonitoringAgent

class SuperAdminAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="SuperAdminAgent")

        # Initialize sub-agents
        self.notifier = NotificationAgent()
        self.logger = LogCollectorAgent()
        self.error_handler = ErrorHandlerAgent(log_collector=self.logger, notifier=self.notifier)
        self.security = SecurityAgent(notifier=self.notifier)
        self.diagnostics = DiagnosticsAgent(notifier=self.notifier)
        self.monitor = MonitoringAgent()

    def health_check(self) -> dict:
        """Get a comprehensive health report"""
        report = {
            "system_status": self.monitor.report(),
            "diagnostics": self.diagnostics.run_health_check()
        }
        self.logger.collect_log("health_check", "info", "Health check completed", report)
        return report

    def handle_exception(self, exception: Exception, source: str, context: dict = None) -> dict:
        """Handle exceptions through the error handler"""
        return self.error_handler.handle_exception(exception, source, context)

    def check_access(self, user_id: str, action: str, resource: str) -> bool:
        """Check if a user has permission to perform an action"""
        return self.security.check_access(user_id, action, resource)

    def notify_user(self, user_id: str, message: str):
        """Send a notification to a user"""
        self.notifier.send_info(user_id, message)
        self.logger.collect_log("notification", "info", f"Notification sent to {user_id}", {"message": message})

    def notify_admin(self, message: str):
        """Send an alert to the administrator"""
        self.notifier.send_alert("admin", message)
        self.logger.collect_log("admin_alert", "warning", "Admin alert sent", {"message": message})

    def run_security_scan(self) -> dict:
        """Run a security vulnerability scan"""
        return self.security.scan_for_vulnerabilities()

    def get_logs(self, level: str = None) -> list:
        """Get collected logs, optionally filtered by level"""
        if level:
            return self.logger.filter_logs(level)
        return self.logger.export_logs()

if __name__ == "__main__":
    # Example usage
    admin = SuperAdminAgent()

    # Test access control
    if not admin.check_access("unauthorized_user", "read", "sensitive_data"):
        admin.notify_admin("Unauthorized access attempt detected!")

    # Test error handling
    try:
        raise ValueError("Test error")
    except Exception as e:
        admin.handle_exception(e, "test_module")

    # Test health check
    health_report = admin.health_check()
    print("Health Report:", health_report)

    # Test notifications
    admin.notify_user("user123", "Welcome to the system!")
    admin.notify_admin("System initialization complete")

    # Test security scan
    security_report = admin.run_security_scan()
    print("Security Report:", security_report)

    # Test logs
    logs = admin.get_logs()
    print(f"Collected {len(logs)} log entries")

