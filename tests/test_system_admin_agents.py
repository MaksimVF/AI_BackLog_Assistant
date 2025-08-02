




import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.super_admin_agent import SuperAdminAgent
from agents.system_admin.error_handler_agent import ErrorHandlerAgent
from agents.system_admin.log_collector_agent import LogCollectorAgent

class TestSystemAdminAgents(unittest.TestCase):
    def setUp(self):
        self.admin = SuperAdminAgent()
        self.error_handler = ErrorHandlerAgent()
        self.log_collector = LogCollectorAgent()

    def test_error_handler(self):
        try:
            raise ValueError("Test value error")
        except Exception as e:
            result = self.error_handler.handle_exception(e, "test_module")

        self.assertEqual(result["exception_type"], "ValueError")
        self.assertIn("Test value error", result["message"])
        self.assertIn("test_module", result["source"])

    def test_log_collector(self):
        self.log_collector.collect_log("test_source", "info", "Test message")
        logs = self.log_collector.export_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["message"], "Test message")

        # Test filtering
        self.log_collector.collect_log("test_source2", "error", "Test error")
        error_logs = self.log_collector.filter_logs("error")
        self.assertEqual(len(error_logs), 1)
        self.assertEqual(error_logs[0]["level"], "ERROR")

    def test_security_access(self):
        # Should allow access
        result = self.admin.check_access("authorized_user", "read", "data")
        self.assertTrue(result)

        # Should deny access and trigger alert
        result = self.admin.check_access("unauthorized_user", "read", "data")
        self.assertFalse(result)

    def test_health_check(self):
        report = self.admin.health_check()
        self.assertIn("system_status", report)
        self.assertIn("diagnostics", report)
        self.assertEqual(report["diagnostics"]["status"], "healthy")

    def test_notifications(self):
        # Test user notification
        self.admin.notify_user("test_user", "Test message")
        logs = self.admin.get_logs()
        self.assertGreater(len(logs), 0)
        self.assertEqual(logs[-1]["message"], "Notification sent to test_user")

        # Test admin alert
        self.admin.notify_admin("Critical system alert")
        logs = self.admin.get_logs()
        self.assertEqual(logs[-1]["message"], "Admin alert sent")

if __name__ == "__main__":
    unittest.main()



