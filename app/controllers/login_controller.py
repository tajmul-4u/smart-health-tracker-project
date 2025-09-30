
import sys
import os

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '../..')
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QLineEdit
from PyQt6.uic.load_ui import loadUiType

try:
    from app.services.api_client import APIClient
except ImportError:
    from services.api_client import APIClient

Ui_LoginWindow, _ = loadUiType(os.path.join(os.path.dirname(__file__), '../ui/login_window.ui'))

class LoginController(QMainWindow, Ui_LoginWindow):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.setupUi(self)

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

        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both email and password")
            return

        try:
            response = self.api_client.login(email, password)
            if response:
                QMessageBox.information(self, "Success", "Login successful!")
                if self.on_login_success:
                    self.on_login_success()
                self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Login Failed", f"Login failed: {str(e)}")

    def show_register_form(self):
        # You can implement a registration form here or use input dialogs for now        
        email, ok1 = QInputDialog.getText(self, 'Register', 'Enter email:')
        if not ok1 or not email:
            return
            
        username, ok2 = QInputDialog.getText(self, 'Register', 'Enter username:')
        if not ok2 or not username:
            return
            
        password, ok3 = QInputDialog.getText(self, 'Register', 'Enter password:', QLineEdit.EchoMode.Password)
        if not ok3 or not password:
            return
            
        full_name, ok4 = QInputDialog.getText(self, 'Register', 'Enter full name:')
        if not ok4 or not full_name:
            return
            
        age, ok5 = QInputDialog.getInt(self, 'Register', 'Enter age:', 25, 1, 120)
        if not ok5:
            return
            
        try:
            user_data = {
                'email': email,
                'username': username,
                'password': password,
                'full_name': full_name,
                'age': age,
                'gender': 'Other',  # Default value
                'weight': 70.0,     # Default value
                'height': 170.0     # Default value
            }
            
            response = self.api_client.register(user_data)
            if response:
                QMessageBox.information(self, "Success", "Registration successful! Please login.")
        except Exception as e:
            QMessageBox.critical(self, "Registration Failed", f"Registration failed: {str(e)}")
