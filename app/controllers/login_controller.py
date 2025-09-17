from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6 import uic
from app.services.api_client import APIClient
import os

class LoginController(QMainWindow):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        
        # Load UI
        ui_path = os.path.join(os.path.dirname(__file__), '../ui/login_window.ui')
        uic.loadUi(ui_path, self)
        
        # Connect signals
        self.loginButton.clicked.connect(self.handle_login)
        self.registerButton.clicked.connect(self.show_register_form)
        
        # Store callback for successful login
        self.on_login_success = None
        
    def set_login_callback(self, callback):
        self.on_login_success = callback
        
    def handle_login(self):
        email = self.emailInput.text()
        password = self.passwordInput.text()
        
        QMessageBox.information(
            self,
            "Backend Not Available",
            "Login is currently disabled as the backend server is not running.\n\n"
            f"Attempted login with:\nEmail: {email}"
        )
            
    def show_register_form(self):
        QMessageBox.information(
            self,
            "Registration Disabled",
            "Registration is currently disabled as the backend server is not running."
        )
