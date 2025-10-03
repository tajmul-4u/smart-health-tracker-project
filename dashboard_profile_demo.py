#!/usr/bin/env python3
"""
Dashboard Profile Health Data Input - Test Application
This simulates the profile section of the dashboard with health data input
"""

import sys
import os
sys.path.insert(0, '/home/tajmul/Projects/Python/health-recomand/smart_health_tracker')

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from app.widgets.health_data_widget import HealthDataInputWidget

class DashboardProfileSimulator(QMainWindow):
    """Simulates the dashboard profile section with health data input"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🏥 Smart Health Tracker - Dashboard Profile Section")
        self.setGeometry(150, 150, 900, 700)
        
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
        
        # Dashboard title
        title_label = QLabel("🏥 Smart Health Tracker Dashboard")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #007bff; margin: 15px;")
        
        # Profile section buttons
        profile_button = QPushButton("👤 Profile")
        profile_button.clicked.connect(self.show_profile_menu)
        
        notifications_button = QPushButton("🔔 Notifications")
        notifications_button.clicked.connect(self.show_notifications)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(notifications_button)
        header_layout.addWidget(profile_button)
        
        main_layout.addLayout(header_layout)
        
        # Dashboard content area
        dashboard_label = QLabel("📊 Dashboard Overview")
        dashboard_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        dashboard_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dashboard_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                margin: 20px;
                color: #666;
            }
        """)
        
        main_layout.addWidget(dashboard_label)
        
        # Instructions
        instructions = QLabel("""
🎯 Click the 'Profile' button above to access:
• 👤 View Profile Information
• 🏥 Update Health Data (Blood Pressure, Blood Sugar, Sleep, etc.)
• ⚙️ Settings
• 🚪 Logout

This simulates the dashboard profile section where users can input health data.
        """)
        instructions.setStyleSheet("""
            QLabel {
                background-color: #e7f3ff;
                border: 1px solid #007bff;
                border-radius: 8px;
                padding: 15px;
                margin: 20px;
                color: #004085;
            }
        """)
        
        main_layout.addWidget(instructions)
        
        # Quick access buttons
        quick_access_layout = QHBoxLayout()
        
        health_data_btn = QPushButton("🏥 Quick Health Data Input")
        health_data_btn.clicked.connect(self.open_health_data_directly)
        health_data_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                font-size: 16px;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        api_test_btn = QPushButton("🔗 Test API Connection")
        api_test_btn.clicked.connect(self.test_api_connection)
        api_test_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                font-size: 14px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        
        quick_access_layout.addWidget(health_data_btn)
        quick_access_layout.addWidget(api_test_btn)
        
        main_layout.addLayout(quick_access_layout)
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        
    def show_profile_menu(self):
        """Show profile menu options"""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction
        
        menu = QMenu(self)
        
        # Profile actions
        view_profile = QAction("👤 View Profile", self)
        view_profile.triggered.connect(self.view_profile)
        menu.addAction(view_profile)
        
        health_data = QAction("🏥 Update Health Data", self)
        health_data.triggered.connect(self.open_health_data_directly)
        menu.addAction(health_data)
        
        settings = QAction("⚙️ Settings", self)
        settings.triggered.connect(self.show_settings)
        menu.addAction(settings)
        
        menu.addSeparator()
        
        logout = QAction("🚪 Logout", self)
        logout.triggered.connect(self.logout)
        menu.addAction(logout)
        
        # Show menu at cursor position
        menu.exec(self.mapFromGlobal(self.cursor().pos()))
        
    def open_health_data_directly(self):
        """Open health data input widget directly"""
        from PyQt6.QtWidgets import QDialog
        
        dialog = QDialog(self)
        dialog.setWindowTitle("🏥 Health Data Input - Dashboard Profile")
        dialog.setModal(True)
        dialog.resize(800, 600)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add health data widget
        health_widget = HealthDataInputWidget()
        
        # Connect signals
        health_widget.data_updated.connect(self.on_health_data_updated)
        health_widget.user_profile_changed.connect(self.on_profile_updated)
        
        layout.addWidget(health_widget)
        
        # Add close button
        close_button = QPushButton("✅ Done")
        close_button.clicked.connect(dialog.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                font-size: 14px;
                padding: 12px 24px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(close_button)
        
        dialog.setLayout(layout)
        dialog.exec()
        
    def on_health_data_updated(self, health_summary):
        """Handle health data updates"""
        QMessageBox.information(
            self,
            "✅ Health Data Updated",
            f"Health data successfully submitted to API!\n\n"
            f"Summary:\n"
            f"• Blood Pressure: {health_summary.get('blood_pressure', 'N/A')}\n"
            f"• Blood Sugar: {health_summary.get('blood_sugar', 'N/A')} mg/dL\n"
            f"• Sleep: {health_summary.get('sleep_hours', 'N/A')} hours\n"
            f"• Steps: {health_summary.get('steps', 'N/A')}\n"
            f"• Mood: {health_summary.get('mood_score', 'N/A')}/10\n\n"
            f"Dashboard would be refreshed with new data."
        )
        
    def on_profile_updated(self, profile_data):
        """Handle profile updates"""
        QMessageBox.information(
            self,
            "✅ Profile Updated",
            f"User profile updated successfully!\n\n"
            f"Updated fields: {', '.join(profile_data.keys())}"
        )
        
    def view_profile(self):
        """Show current profile information"""
        import requests
        
        try:
            response = requests.get("http://localhost:8000/api/users/me", timeout=5)
            if response.status_code == 200:
                user_data = response.json()
                
                profile_info = f"""
👤 Current User Profile

📧 Email: {user_data.get('email', 'Not set')}
👤 Username: {user_data.get('username', 'Not set')}
📛 Full Name: {user_data.get('full_name', 'Not set')}
🎂 Age: {user_data.get('age', 'Not set')} years
⚥ Gender: {user_data.get('gender', 'Not set')}
📏 Height: {user_data.get('height', 'Not set')} cm
⚖️ Weight: {user_data.get('weight', 'Not set')} kg

✏️ Click 'Update Health Data' to modify your information.
                """
                
                QMessageBox.information(self, "👤 Profile Information", profile_info)
            else:
                QMessageBox.warning(self, "⚠️ Warning", "Could not load user profile from API")
                
        except Exception as e:
            QMessageBox.critical(self, "❌ Error", f"Failed to connect to API:\n{str(e)}")
            
    def show_notifications(self):
        """Show notifications"""
        QMessageBox.information(
            self,
            "🔔 Notifications",
            "📢 Recent Notifications:\n\n"
            "• 🏥 Time for your evening medication (5 mins ago)\n"
            "• 🎯 You've reached your daily step goal! (2 hours ago)\n"
            "• 📝 Don't forget to log your blood pressure (1 day ago)\n\n"
            "All notifications are up to date!"
        )
        
    def show_settings(self):
        """Show settings"""
        QMessageBox.information(
            self,
            "⚙️ Settings",
            "🔧 Application Settings:\n\n"
            "• 🔔 Notification preferences\n"
            "• 📊 Data export/import\n"
            "• 🔒 Privacy settings\n"
            "• 🎨 Theme preferences\n"
            "• 🌐 Language settings\n\n"
            "Settings panel would open here."
        )
        
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            "🚪 Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "👋 Goodbye", "You have been logged out successfully!")
            self.close()
            
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
                    f"📖 Documentation: http://localhost:8000/docs"
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
                f"python main_enhanced.py"
            )

def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Smart Health Tracker Dashboard")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Health Tracker Inc.")
    
    # Create and show main window
    window = DashboardProfileSimulator()
    window.show()
    
    # Start the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()