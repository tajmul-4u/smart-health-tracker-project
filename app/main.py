import sys
import os
from PyQt6.QtWidgets import QApplication

# Add the project root to Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

# Now we can import with the full path
try:
    from app.controllers.login_controller import LoginController
    from app.controllers.working_dashboard_controller import WorkingDashboardController
    from app.services.api_client import APIClient
except ImportError:
    # Fallback to simple relative imports
    from controllers.login_controller import LoginController
    from controllers.working_dashboard_controller import WorkingDashboardController
    from services.api_client import APIClient

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
            
        # Show modern dashboard
        self.dashboard = WorkingDashboardController(self.api_client)
        self.dashboard.show()

if __name__ == "__main__":
    app = SmartHealthTracker()
    sys.exit(app.start())
