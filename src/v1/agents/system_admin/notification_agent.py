




import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseAgent



class NotificationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="NotificationAgent")

    def send_alert(self, category: str, message: str):
        # For now just print, but can be replaced with actual sending
        print(f"[{category.upper()}] Alert: {message}")

    def send_info(self, user_id: str, message: str):
        print(f"[INFO] -> {user_id}: {message}")

    def notify_admin(self, message: str):
        """Special method to notify system administrator"""
        self.send_alert("ADMIN", message)


