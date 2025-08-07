


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
from system_admin.self_healing_agent import SelfHealingAgent

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
        self.self_healing = SelfHealingAgent()

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

    def check_self_healing(self) -> dict:
        """Check if self-healing actions are needed"""
        return self.self_healing.check_system_health()

    def perform_self_healing(self) -> dict:
        """Perform automatic self-healing actions"""
        health_check = self.check_self_healing()
        actions = health_check.get('actions_needed', [])
        results = self.self_healing.perform_self_healing(actions)
        return {
            'health_check': health_check,
            'actions_taken': results
        }

    def restart_service(self, service_name: str) -> dict:
        """Restart a specific service"""
        return self.self_healing.restart_service(service_name)

    def trigger_failover(self, service_name: str) -> dict:
        """Trigger failover for a critical service"""
        return self.self_healing.trigger_failover(service_name)

    def auto_scale_resources(self, resource_type: str, amount: int) -> dict:
        """Automatically scale resources"""
        return self.self_healing.auto_scale_resources(resource_type, amount)

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

    # Test self-healing capabilities
    print("\n=== Testing Self-Healing Capabilities ===")

    # Check if self-healing is needed
    healing_check = admin.check_self_healing()
    print("Self-Healing Check:", healing_check)

    # Perform automatic self-healing
    if healing_check.get('actions_needed'):
        print(f"Actions needed: {len(healing_check['actions_needed'])}")
        healing_results = admin.perform_self_healing()
        print("Self-Healing Results:", healing_results)
    else:
        print("No self-healing actions needed at this time")

    # Test service restart
    service_result = admin.restart_service("test_service")
    print("Service Restart Result:", service_result)

    # Test failover
    failover_result = admin.trigger_failover("database_service")
    print("Failover Result:", failover_result)

    # Test auto-scaling
    scale_result = admin.auto_scale_resources("memory", 4)
    print("Auto-Scale Result:", scale_result)

