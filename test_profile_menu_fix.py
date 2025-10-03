#!/usr/bin/env python3
"""
Test Profile Menu Fix - Health Data Input Visibility
Verifies that the profile menu shows the health data input option
"""

import sys
import os
sys.path.append('/home/tajmul/Projects/Python/health-recomand/smart_health_tracker')

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt
from app.controllers.enhanced_dashboard_controller import EnhancedDashboardController
from app.services.api_client import APIClient

class ProfileMenuTestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏥 Profile Menu Test - Health Data Input Visibility")
        self.setGeometry(200, 200, 500, 300)
        
        # Create mock API client
        api_client = APIClient("http://localhost:8000")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🧪 Profile Menu Test")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            margin: 20px;
            padding: 10px;
            background-color: #e7f3ff;
            border: 2px solid #007bff;
            border-radius: 8px;
        """)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("""
📋 Test Instructions:
1. Click 'Open Dashboard' to open the main dashboard
2. Click on the profile icon/name (top-right area)
3. Verify the menu shows:
   • 👤 Edit Profile (Primary option)
   • 🏥 Health Data (Input option) ← This should be visible!
   • 📋 View Profile Info
   • ⚙️ Settings
   • 🚪 Logout

🎯 Expected Result: The "🏥 Health Data" option should be visible in the profile menu.
        """)
        instructions.setStyleSheet("""
            font-size: 12px;
            padding: 15px;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            margin: 10px;
        """)
        layout.addWidget(instructions)
        
        # Test button
        test_button = QPushButton("🚀 Open Dashboard (Test Profile Menu)")
        test_button.clicked.connect(self.open_dashboard)
        test_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(test_button)
        
        # Status
        self.status_label = QLabel("Status: Ready to test")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            font-weight: bold;
            padding: 10px;
            margin: 10px;
            border-radius: 4px;
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
        """)
        layout.addWidget(self.status_label)
        
    def open_dashboard(self):
        try:
            # Create API client
            api_client = APIClient("http://localhost:8000")
            
            # Create dashboard
            self.dashboard = EnhancedDashboardController(api_client)
            
            # Mock some user data
            self.dashboard.current_user = {
                'full_name': 'Test User',
                'email': 'test@example.com'
            }
            
            # Update status
            self.status_label.setText("✅ Dashboard opened! Click profile icon/name to test menu")
            self.status_label.setStyleSheet("""
                font-weight: bold;
                padding: 10px;
                margin: 10px;
                border-radius: 4px;
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
            """)
            
            # Show dashboard
            self.dashboard.show()
            
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
            self.status_label.setStyleSheet("""
                font-weight: bold;
                padding: 10px;
                margin: 10px;
                border-radius: 4px;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
            """)
            print(f"Error opening dashboard: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    print("🧪 Starting Profile Menu Test...")
    print("📋 This test verifies that the health data input option is visible in the profile menu")
    
    test_app = ProfileMenuTestApp()
    test_app.show()
    
    print("✅ Test application started")
    print("👆 Click 'Open Dashboard' then test the profile menu")
    
    sys.exit(app.exec())