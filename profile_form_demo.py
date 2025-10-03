#!/usr/bin/env python3
"""
Profile Form Demo - Standalone test for the new profile form functionality
"""

import sys
import os
sys.path.insert(0, '/home/tajmul/Projects/Python/health-recomand/smart_health_tracker')

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from app.widgets.user_profile_form import UserProfileFormWidget

class ProfileFormDemo(QMainWindow):
    """Demo application for the profile form"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("👤 Profile Form Demo - Smart Health Tracker")
        self.setGeometry(100, 100, 1000, 800)
        
        # Set style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #333;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("👤 User Profile Management Demo")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #007bff; margin: 15px;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Description
        description = QLabel("""
🎯 This demo shows the new profile form functionality for Smart Health Tracker.

✅ <b>What's New:</b>
• Profile menu now prioritizes user input form over settings/logout
• Comprehensive profile management with tabbed interface
• Personal info, contact details, health profile, and preferences
• Real-time API integration for saving and updating data
• Form validation and user-friendly error handling

✅ <b>Profile Menu Structure (Updated):</b>
• <b>👤 Edit Profile</b> - Primary action (bold, top of menu)
• 🏥 Health Data - Secondary health tracking
• 📋 View Profile Info - Quick profile overview
• ⚙️ Settings - Application settings
• 🚪 Logout - Session termination

Click "Open Profile Form" below to see the comprehensive profile management interface.
        """)
        description.setStyleSheet("""
            QLabel {
                background-color: #e7f3ff;
                border: 1px solid #007bff;
                border-radius: 8px;
                padding: 20px;
                margin: 20px;
                color: #004085;
                line-height: 1.6;
            }
        """)
        description.setWordWrap(True)
        
        main_layout.addWidget(description)
        
        # Demo buttons
        button_layout = QHBoxLayout()
        
        profile_form_btn = QPushButton("👤 Open Profile Form")
        profile_form_btn.clicked.connect(self.open_profile_form)
        profile_form_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                font-size: 16px;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        simulate_menu_btn = QPushButton("📋 Simulate Profile Menu")
        simulate_menu_btn.clicked.connect(self.simulate_profile_menu)
        simulate_menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                font-size: 14px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        
        api_test_btn = QPushButton("🔗 Test API Connection")
        api_test_btn.clicked.connect(self.test_api_connection)
        api_test_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                font-size: 14px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        button_layout.addWidget(profile_form_btn)
        button_layout.addWidget(simulate_menu_btn)
        button_layout.addWidget(api_test_btn)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        
    def open_profile_form(self):
        """Open the comprehensive profile form"""
        from PyQt6.QtWidgets import QDialog
        
        dialog = QDialog(self)
        dialog.setWindowTitle("👤 User Profile Management")
        dialog.setModal(True)
        dialog.resize(900, 700)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add profile form widget
        profile_form = UserProfileFormWidget()
        
        # Connect signals
        profile_form.profile_saved.connect(self.on_profile_saved)
        profile_form.profile_updated.connect(self.on_profile_updated)
        
        layout.addWidget(profile_form)
        
        # Add close button
        close_button = QPushButton("✅ Close")
        close_button.clicked.connect(dialog.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(close_button)
        
        dialog.setLayout(layout)
        dialog.exec()
        
    def simulate_profile_menu(self):
        """Simulate the new profile menu structure"""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction
        
        menu = QMenu(self)
        
        # Primary Profile Form Action (bold)
        profile_form_action = QAction("👤 Edit Profile", self)
        profile_form_action.triggered.connect(self.open_profile_form)
        font = QFont("Arial", 10, QFont.Weight.Bold)
        profile_form_action.setFont(font)
        menu.addAction(profile_form_action)
        
        menu.addSeparator()
        
        # Secondary actions
        health_data_action = QAction("🏥 Health Data", self)
        health_data_action.triggered.connect(lambda: self.show_message("Health Data", "Health data tracking would open here"))
        menu.addAction(health_data_action)
        
        view_profile_action = QAction("📋 View Profile Info", self)
        view_profile_action.triggered.connect(lambda: self.show_message("Profile Info", "Quick profile overview would show here"))
        menu.addAction(view_profile_action)
        
        menu.addSeparator()
        
        # Bottom actions
        settings_action = QAction("⚙️ Settings", self)
        settings_action.triggered.connect(lambda: self.show_message("Settings", "Application settings would open here"))
        menu.addAction(settings_action)
        
        logout_action = QAction("🚪 Logout", self)
        logout_action.triggered.connect(lambda: self.show_message("Logout", "User would be logged out"))
        menu.addAction(logout_action)
        
        # Show menu
        menu.exec(self.mapFromGlobal(self.cursor().pos()))
        
    def show_message(self, title, message):
        """Show a simple message"""
        QMessageBox.information(self, title, message)
        
    def on_profile_saved(self, profile_data):
        """Handle profile save events"""
        QMessageBox.information(
            self,
            "✅ Profile Saved",
            f"Profile information saved successfully!\n\n"
            f"Name: {profile_data.get('full_name', 'N/A')}\n"
            f"Email: {profile_data.get('email', 'N/A')}\n"
            f"Phone: {profile_data.get('phone', 'N/A')}\n"
            f"Height: {profile_data.get('height', 'N/A')} cm\n"
            f"Weight: {profile_data.get('weight', 'N/A')} kg"
        )
        
    def on_profile_updated(self, profile_data):
        """Handle profile update events"""
        print(f"Profile updated: {profile_data.get('full_name', 'Unknown')}")
        
    def test_api_connection(self):
        """Test API connection"""
        import requests
        
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(
                    self,
                    "✅ API Connection",
                    f"✅ Backend API is running!\n\n"
                    f"Status: {data.get('status', 'Unknown')}\n"
                    f"Database: {data.get('database', 'Unknown')}\n\n"
                    f"🔗 API URL: http://localhost:8000\n"
                    f"📖 Documentation: http://localhost:8000/docs\n\n"
                    f"Profile form can save data to the API!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "⚠️ API Warning",
                    f"API responded with status code: {response.status_code}"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ API Error",
                f"Could not connect to backend API:\n{str(e)}\n\n"
                f"Make sure the backend is running:\n"
                f"cd backend_api\n"
                f"python main_enhanced.py\n\n"
                f"Profile form will work offline but won't save to database."
            )

def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Profile Form Demo")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Smart Health Tracker")
    
    # Create and show main window
    window = ProfileFormDemo()
    window.show()
    
    # Start the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()