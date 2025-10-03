#!/usr/bin/env python3
"""
Comprehensive Profile Management Demo
Shows the modern professional design and user-friendly profile management
"""

import sys
import os
sys.path.insert(0, '/home/tajmul/Projects/Python/health-recomand/smart_health_tracker')

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLabel, QMessageBox, QFrame, QScrollArea, QGridLayout,
    QGroupBox, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QBrush

class ProfileManagementShowcase(QMainWindow):
    """Showcase of the profile management with modern professional design"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the showcase UI"""
        self.setWindowTitle("🏥 Smart Health Tracker - Profile Management Showcase")
        self.setGeometry(100, 100, 1200, 900)
        
        # Apply modern professional styling
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #f8f9fa, stop: 1 #e9ecef);
            }
            
            QWidget {
                font-family: 'Segoe UI', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            .header {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 #667eea, stop: 1 #764ba2);
                color: white;
                border-radius: 12px;
                padding: 20px;
                margin: 10px;
            }
            
            .feature-card {
                background: white;
                border: 1px solid #e1e5e9;
                border-radius: 16px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .feature-card:hover {
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
                transform: translateY(-2px);
            }
            
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #4facfe, stop: 1 #00f2fe);
                color: white;
                border: none;
                padding: 14px 28px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                margin: 8px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #667eea, stop: 1 #764ba2);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #5a67d8, stop: 1 #553c9a);
            }
            
            .primary-button {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #56cc9d, stop: 1 #6eaa5d);
                font-size: 16px;
                padding: 16px 32px;
                border-radius: 12px;
            }
            
            .primary-button:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #48bb92, stop: 1 #5e9a52);
            }
            
            .secondary-button {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #ffeaa7, stop: 1 #fab1a0);
                color: #2d3436;
            }
            
            .secondary-button:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #fdcb6e, stop: 1 #e84393);
                color: white;
            }
            
            QLabel {
                color: #2d3436;
            }
            
            .title {
                font-size: 24px;
                font-weight: bold;
                color: white;
                margin-bottom: 10px;
            }
            
            .subtitle {
                font-size: 16px;
                color: rgba(255, 255, 255, 0.9);
                margin-bottom: 20px;
            }
            
            .feature-title {
                font-size: 18px;
                font-weight: bold;
                color: #2d3436;
                margin-bottom: 12px;
            }
            
            .feature-description {
                font-size: 14px;
                color: #636e72;
                line-height: 1.6;
                margin-bottom: 15px;
            }
            
            QTextEdit {
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                background: #f8f9fa;
                font-size: 13px;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Main content widget
        content_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Header section
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Features showcase
        features = self.create_features_showcase()
        main_layout.addWidget(features)
        
        # Demo buttons
        demo_section = self.create_demo_section()
        main_layout.addWidget(demo_section)
        
        # Footer
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        content_widget.setLayout(main_layout)
        scroll.setWidget(content_widget)
        
        # Set scroll as central widget
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        central_widget.setLayout(layout)
        
    def create_header(self):
        """Create the header section"""
        header = QFrame()
        header.setProperty("class", "header")
        layout = QVBoxLayout()
        
        title = QLabel("🏥 Smart Health Tracker")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Modern Professional Profile Management System")
        subtitle.setProperty("class", "subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description = QLabel("""
✨ Experience our comprehensive profile management with modern design
🎯 User-friendly interface with professional-grade functionality
🔒 Secure data handling with real-time API integration
        """)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px; margin: 15px;")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(description)
        
        header.setLayout(layout)
        return header
        
    def create_features_showcase(self):
        """Create the features showcase section"""
        features_widget = QWidget()
        grid_layout = QGridLayout()
        
        # Feature cards data
        features = [
            {
                "icon": "👤",
                "title": "Personal Information",
                "description": "Complete personal details management with modern form controls. Input name, gender, height, weight, and birth date with intuitive validation.",
                "highlights": ["Modern form controls", "Real-time validation", "Professional styling"]
            },
            {
                "icon": "📞",
                "title": "Contact Management",
                "description": "Comprehensive contact information including email, phone, address, and emergency contacts. Smart validation ensures data accuracy.",
                "highlights": ["Email validation", "Emergency contacts", "Address management"]
            },
            {
                "icon": "🏥",
                "title": "Health Profile",
                "description": "Detailed health information including blood type, allergies, medications, and health goals. Professional medical data management.",
                "highlights": ["Medical history", "Allergy tracking", "Goal setting"]
            },
            {
                "icon": "⚙️",
                "title": "Smart Preferences",
                "description": "Customizable preferences for notifications, privacy settings, and display options. Personalize your health tracking experience.",
                "highlights": ["Notification control", "Privacy settings", "Display options"]
            }
        ]
        
        for i, feature in enumerate(features):
            card = self.create_feature_card(feature)
            row = i // 2
            col = i % 2
            grid_layout.addWidget(card, row, col)
            
        features_widget.setLayout(grid_layout)
        return features_widget
        
    def create_feature_card(self, feature_data):
        """Create a feature card"""
        card = QFrame()
        card.setProperty("class", "feature-card")
        layout = QVBoxLayout()
        
        # Icon and title
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(feature_data["icon"])
        icon_label.setStyleSheet("font-size: 32px; margin-right: 10px;")
        
        title_label = QLabel(feature_data["title"])
        title_label.setProperty("class", "feature-title")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Description
        desc_label = QLabel(feature_data["description"])
        desc_label.setProperty("class", "feature-description")
        desc_label.setWordWrap(True)
        
        # Highlights
        highlights_text = "✨ " + " • ".join(feature_data["highlights"])
        highlights_label = QLabel(highlights_text)
        highlights_label.setStyleSheet("color: #00b894; font-weight: 600; font-size: 12px; margin-top: 10px;")
        highlights_label.setWordWrap(True)
        
        layout.addLayout(header_layout)
        layout.addWidget(desc_label)
        layout.addWidget(highlights_label)
        
        card.setLayout(layout)
        return card
        
    def create_demo_section(self):
        """Create the demo section"""
        demo_widget = QFrame()
        demo_widget.setProperty("class", "feature-card")
        layout = QVBoxLayout()
        
        title = QLabel("🚀 Experience the Profile Management")
        title.setProperty("class", "feature-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description = QLabel("""
Try our comprehensive profile management system with modern professional design.
Click the buttons below to experience different aspects of the system.
        """)
        description.setProperty("class", "feature-description")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Open Profile Form button
        profile_btn = QPushButton("👤 Open Profile Form")
        profile_btn.setProperty("class", "primary-button")
        profile_btn.clicked.connect(self.open_profile_form)
        
        # Show Menu Structure button
        menu_btn = QPushButton("📋 Profile Menu Demo")
        menu_btn.setProperty("class", "secondary-button")
        menu_btn.clicked.connect(self.show_menu_structure)
        
        # API Test button
        api_btn = QPushButton("🔗 Test API Connection")
        api_btn.clicked.connect(self.test_api_connection)
        
        button_layout.addWidget(profile_btn)
        button_layout.addWidget(menu_btn)
        button_layout.addWidget(api_btn)
        
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(button_layout)
        
        demo_widget.setLayout(layout)
        return demo_widget
        
    def create_footer(self):
        """Create the footer section"""
        footer = QFrame()
        footer.setProperty("class", "feature-card")
        layout = QVBoxLayout()
        
        title = QLabel("🎯 Modern Professional Design Features")
        title.setProperty("class", "feature-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        features_text = QTextEdit()
        features_text.setReadOnly(True)
        features_text.setMaximumHeight(200)
        
        features_content = """
✨ MODERN DESIGN ELEMENTS:
• Gradient backgrounds and smooth transitions
• Professional color scheme with accessibility in mind
• Responsive layout that adapts to different screen sizes
• Subtle shadows and hover effects for visual depth

🎨 USER-FRIENDLY FEATURES:
• Intuitive tabbed interface for organized data entry
• Clear visual hierarchy with proper typography
• Form validation with helpful error messages
• Progress indicators and success confirmations

🔧 PROFESSIONAL FUNCTIONALITY:
• Real-time API integration for data persistence
• Comprehensive form fields for all profile aspects
• Smart validation preventing invalid data entry
• Secure handling of sensitive health information

🚀 ENHANCED USER EXPERIENCE:
• Smooth animations and micro-interactions
• Contextual tooltips and help text
• Keyboard navigation support
• Mobile-responsive design principles
        """
        
        features_text.setPlainText(features_content)
        
        layout.addWidget(title)
        layout.addWidget(features_text)
        
        footer.setLayout(layout)
        return footer
        
    def open_profile_form(self):
        """Open the comprehensive profile form"""
        try:
            from app.widgets.user_profile_form import UserProfileFormWidget
            from PyQt6.QtWidgets import QDialog
            
            dialog = QDialog(self)
            dialog.setWindowTitle("👤 Professional Profile Management")
            dialog.setModal(True)
            dialog.resize(950, 750)
            
            # Apply modern dialog styling
            dialog.setStyleSheet("""
                QDialog {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #f8f9fa, stop: 1 #e9ecef);
                    border-radius: 12px;
                }
            """)
            
            layout = QVBoxLayout()
            
            # Add profile form
            profile_form = UserProfileFormWidget()
            
            # Connect signals for demo
            profile_form.profile_saved.connect(self.on_profile_saved)
            profile_form.profile_updated.connect(self.on_profile_updated)
            
            layout.addWidget(profile_form)
            
            # Modern close button
            close_button = QPushButton("✅ Close")
            close_button.clicked.connect(dialog.accept)
            close_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #56cc9d, stop: 1 #6eaa5d);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #48bb92, stop: 1 #5e9a52);
                }
            """)
            
            layout.addWidget(close_button)
            dialog.setLayout(layout)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open profile form:\n{str(e)}")
            
    def show_menu_structure(self):
        """Show the profile menu structure"""
        QMessageBox.information(
            self,
            "📋 Profile Menu Structure",
            """
🎯 NEW PROFILE MENU STRUCTURE:

👤 Edit Profile (PRIMARY - Bold, Comprehensive Form)
├─────────────────────────────────────────────
├─ 🏥 Health Data (Secondary Health Tracking)
├─ 📋 View Profile Info (Quick Profile Overview)
├─────────────────────────────────────────────
├─ ⚙️ Settings (Application Preferences)
└─ 🚪 Logout (Session Termination)

✨ Key Improvements:
• Profile form is now the PRIMARY action
• Bold styling emphasizes importance
• Comprehensive 4-tab interface
• Modern professional design
• User-friendly validation
• Real-time API integration

🎯 The profile form includes:
• Personal Information Tab
• Contact Information Tab  
• Health Profile Tab
• Preferences Tab

Click "Open Profile Form" to experience it!
            """
        )
        
    def test_api_connection(self):
        """Test API connection"""
        import requests
        
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(
                    self,
                    "✅ API Connection Success",
                    f"""
🚀 Backend API is running perfectly!

📊 API Status:
• Status: {data.get('status', 'Unknown')}
• Database: {data.get('database', 'Unknown')}
• Connection: Healthy

🔗 API Details:
• URL: http://localhost:8000
• Documentation: http://localhost:8000/docs
• Health Check: ✅ PASSED

✨ Profile Form Benefits:
• Real-time data saving
• Automatic form population
• Data validation
• Error handling
• Progress feedback

The profile management system is fully operational!
                    """
                )
            else:
                QMessageBox.warning(self, "⚠️ API Warning", f"API responded with status: {response.status_code}")
        except Exception as e:
            QMessageBox.information(
                self,
                "🔧 API Connection",
                f"""
⚠️ Backend API not detected.

🔍 Status: Not running or unreachable
📝 Error: {str(e)}

💡 To enable full functionality:
1. Start the backend: cd backend_api && python main_enhanced.py
2. Profile form will work offline but won't save to database

🎯 Current capabilities:
• ✅ Profile form display
• ✅ Form validation
• ✅ Data collection
• ❌ API saving (offline mode)

The profile form will still demonstrate all features!
                """
            )
            
    def on_profile_saved(self, profile_data):
        """Handle profile save events"""
        QMessageBox.information(
            self,
            "✅ Profile Saved Successfully",
            f"""
🎉 Your profile has been saved!

👤 Profile Details:
• Name: {profile_data.get('full_name', 'N/A')}
• Email: {profile_data.get('email', 'N/A')}
• Phone: {profile_data.get('phone', 'N/A')}
• Height: {profile_data.get('height', 'N/A')} cm
• Weight: {profile_data.get('weight', 'N/A')} kg

✨ Modern Features Demonstrated:
• Professional form validation ✅
• Real-time data processing ✅  
• User-friendly feedback ✅
• Secure data handling ✅

Your Smart Health Tracker profile is now complete!
            """
        )
        
    def on_profile_updated(self, profile_data):
        """Handle profile update events"""
        print(f"Profile updated: {profile_data.get('full_name', 'Unknown User')}")

def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Profile Management Showcase")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Smart Health Tracker")
    
    # Create and show showcase
    showcase = ProfileManagementShowcase()
    showcase.show()
    
    # Add a timer to show a welcome message
    QTimer.singleShot(1000, lambda: QMessageBox.information(
        showcase,
        "🏥 Welcome to Smart Health Tracker",
        """
🎉 Welcome to the Profile Management Showcase!

This demo demonstrates our modern professional profile management system with:

✨ Modern Professional Design
🎯 User-Friendly Interface  
🔒 Secure Data Management
🚀 Real-Time API Integration

Click "Open Profile Form" to experience the comprehensive profile management interface!
        """
    ))
    
    # Start the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()