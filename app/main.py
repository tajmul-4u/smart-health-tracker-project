import sys
from PyQt6.QtWidgets import QApplication
import sys
from app.controllers.login_controller import LoginController
from app.controllers.dashboard_controller import DashboardController
from app.services.api_client import APIClient

class SmartHealthTracker:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.api_client = APIClient()
        self.login_window = None
        self.dashboard = None
        
    def start(self):
        # Create and show login window
        self.login_window = LoginController(self.api_client)
        self.login_window.set_login_callback(self.on_login_success)
        self.login_window.show()
        
        # Start event loop
        return self.app.exec()
        
    def on_login_success(self):
        # Hide login window
        if self.login_window:
            self.login_window.hide()
            
        # Show dashboard
        self.dashboard = DashboardController(self.api_client)
        self.dashboard.show()

if __name__ == "__main__":
    app = SmartHealthTracker()
    sys.exit(app.start())
