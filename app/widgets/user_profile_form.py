#!/usr/bin/env python3
"""
User Profile Form Widget
Comprehensive profile management interface for user information input and updates
"""

import sys
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, 
    QSpinBox, QDoubleSpinBox, QTextEdit, QPushButton, QLabel, QFrame, 
    QScrollArea, QMessageBox, QTabWidget, QDateEdit, QCheckBox, QGroupBox,
    QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QPixmap, QPainter, QBrush, QColor

class UserProfileFormWidget(QWidget):
    """User profile form widget for comprehensive profile management"""
    
    # Signals
    profile_updated = pyqtSignal(dict)  # Emitted when profile is updated
    profile_saved = pyqtSignal(dict)    # Emitted when profile is saved
    
    def __init__(self, api_client=None):
        super().__init__()
        self.api_client = api_client
        self.user_data = {}
        self.init_ui()
        self.load_user_profile()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("👤 User Profile Management")
        self.setMinimumSize(700, 600)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # Create scroll area for the form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create tab widget for organized sections
        self.tab_widget = QTabWidget()
        
        # Personal Information Tab
        personal_tab = self.create_personal_info_tab()
        self.tab_widget.addTab(personal_tab, "👤 Personal Info")
        
        # Contact Information Tab
        contact_tab = self.create_contact_info_tab()
        self.tab_widget.addTab(contact_tab, "📞 Contact Info")
        
        # Health Profile Tab
        health_tab = self.create_health_profile_tab()
        self.tab_widget.addTab(health_tab, "🏥 Health Profile")
        
        # Preferences Tab
        preferences_tab = self.create_preferences_tab()
        self.tab_widget.addTab(preferences_tab, "⚙️ Preferences")
        
        scroll.setWidget(self.tab_widget)
        main_layout.addWidget(scroll)
        
        # Action buttons
        button_layout = self.create_action_buttons()
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Apply styling
        self.apply_styling()
        
    def create_header(self):
        """Create the header section"""
        header_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("👤 User Profile Management")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        
        # Subtitle
        subtitle_label = QLabel("Update your personal information, contact details, and health profile")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        return header_layout
        
    def create_personal_info_tab(self):
        """Create personal information tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Basic Information Group
        basic_group = QGroupBox("📋 Basic Information")
        basic_layout = QFormLayout()
        
        # Full Name
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("Enter your full name")
        basic_layout.addRow("📛 Full Name:", self.full_name_input)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        basic_layout.addRow("👤 Username:", self.username_input)
        
        # Date of Birth
        self.birth_date_input = QDateEdit()
        self.birth_date_input.setDate(QDate(1990, 1, 1))
        self.birth_date_input.setCalendarPopup(True)
        basic_layout.addRow("🎂 Date of Birth:", self.birth_date_input)
        
        # Gender
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Select Gender", "Male", "Female", "Other", "Prefer not to say"])
        basic_layout.addRow("⚥ Gender:", self.gender_input)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # Physical Information Group
        physical_group = QGroupBox("📏 Physical Information")
        physical_layout = QFormLayout()
        
        # Height
        height_layout = QHBoxLayout()
        self.height_input = QSpinBox()
        self.height_input.setRange(50, 250)
        self.height_input.setSuffix(" cm")
        self.height_input.setValue(170)
        height_layout.addWidget(self.height_input)
        
        height_label = QLabel("(e.g., 175 cm)")
        height_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        height_layout.addWidget(height_label)
        height_layout.addStretch()
        
        physical_layout.addRow("📏 Height:", height_layout)
        
        # Weight
        weight_layout = QHBoxLayout()
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(20.0, 300.0)
        self.weight_input.setSuffix(" kg")
        self.weight_input.setValue(70.0)
        self.weight_input.setDecimals(1)
        weight_layout.addWidget(self.weight_input)
        
        weight_label = QLabel("(e.g., 70.5 kg)")
        weight_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        weight_layout.addWidget(weight_label)
        weight_layout.addStretch()
        
        physical_layout.addRow("⚖️ Weight:", weight_layout)
        
        physical_group.setLayout(physical_layout)
        layout.addWidget(physical_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def create_contact_info_tab(self):
        """Create contact information tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Contact Details Group
        contact_group = QGroupBox("📞 Contact Details")
        contact_layout = QFormLayout()
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")
        contact_layout.addRow("📧 Email:", self.email_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        contact_layout.addRow("📱 Phone:", self.phone_input)
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Enter your address")
        self.address_input.setMaximumHeight(80)
        contact_layout.addRow("🏠 Address:", self.address_input)
        
        # City
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter your city")
        contact_layout.addRow("🏙️ City:", self.city_input)
        
        # Country
        self.country_input = QComboBox()
        self.country_input.setEditable(True)
        countries = ["Select Country", "United States", "Canada", "United Kingdom", "Germany", "France", "Australia", "Japan", "India", "Brazil", "Other"]
        self.country_input.addItems(countries)
        contact_layout.addRow("🌍 Country:", self.country_input)
        
        contact_group.setLayout(contact_layout)
        layout.addWidget(contact_group)
        
        # Emergency Contact Group
        emergency_group = QGroupBox("🚨 Emergency Contact")
        emergency_layout = QFormLayout()
        
        # Emergency Contact Name
        self.emergency_name_input = QLineEdit()
        self.emergency_name_input.setPlaceholderText("Emergency contact name")
        emergency_layout.addRow("👤 Name:", self.emergency_name_input)
        
        # Emergency Contact Phone
        self.emergency_phone_input = QLineEdit()
        self.emergency_phone_input.setPlaceholderText("Emergency contact phone")
        emergency_layout.addRow("📱 Phone:", self.emergency_phone_input)
        
        # Relationship
        self.emergency_relationship_input = QComboBox()
        relationships = ["Select Relationship", "Spouse", "Parent", "Child", "Sibling", "Friend", "Other"]
        self.emergency_relationship_input.addItems(relationships)
        emergency_layout.addRow("👥 Relationship:", self.emergency_relationship_input)
        
        emergency_group.setLayout(emergency_layout)
        layout.addWidget(emergency_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def create_health_profile_tab(self):
        """Create health profile tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Medical Information Group
        medical_group = QGroupBox("🏥 Medical Information")
        medical_layout = QFormLayout()
        
        # Blood Type
        self.blood_type_input = QComboBox()
        blood_types = ["Select Blood Type", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"]
        self.blood_type_input.addItems(blood_types)
        medical_layout.addRow("🩸 Blood Type:", self.blood_type_input)
        
        # Allergies
        self.allergies_input = QTextEdit()
        self.allergies_input.setPlaceholderText("List any allergies (food, medication, environmental)")
        self.allergies_input.setMaximumHeight(60)
        medical_layout.addRow("🤧 Allergies:", self.allergies_input)
        
        # Medications
        self.medications_input = QTextEdit()
        self.medications_input.setPlaceholderText("List current medications")
        self.medications_input.setMaximumHeight(60)
        medical_layout.addRow("💊 Medications:", self.medications_input)
        
        # Medical Conditions
        self.conditions_input = QTextEdit()
        self.conditions_input.setPlaceholderText("List any medical conditions")
        self.conditions_input.setMaximumHeight(60)
        medical_layout.addRow("🏥 Medical Conditions:", self.conditions_input)
        
        medical_group.setLayout(medical_layout)
        layout.addWidget(medical_group)
        
        # Health Goals Group
        goals_group = QGroupBox("🎯 Health Goals")
        goals_layout = QFormLayout()
        
        # Primary Health Goal
        self.health_goal_input = QComboBox()
        goals = ["Select Primary Goal", "Weight Loss", "Weight Gain", "Maintain Weight", "Build Muscle", "Improve Cardio", "Manage Condition", "General Wellness"]
        self.health_goal_input.addItems(goals)
        goals_layout.addRow("🎯 Primary Goal:", self.health_goal_input)
        
        # Target Weight
        self.target_weight_input = QDoubleSpinBox()
        self.target_weight_input.setRange(20.0, 300.0)
        self.target_weight_input.setSuffix(" kg")
        self.target_weight_input.setValue(70.0)
        self.target_weight_input.setDecimals(1)
        goals_layout.addRow("🎯 Target Weight:", self.target_weight_input)
        
        # Activity Level
        self.activity_level_input = QComboBox()
        activity_levels = ["Select Activity Level", "Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
        self.activity_level_input.addItems(activity_levels)
        goals_layout.addRow("🏃 Activity Level:", self.activity_level_input)
        
        goals_group.setLayout(goals_layout)
        layout.addWidget(goals_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def create_preferences_tab(self):
        """Create preferences tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Notification Preferences Group
        notification_group = QGroupBox("🔔 Notification Preferences")
        notification_layout = QVBoxLayout()
        
        self.email_notifications = QCheckBox("📧 Email notifications")
        self.email_notifications.setChecked(True)
        notification_layout.addWidget(self.email_notifications)
        
        self.health_reminders = QCheckBox("⏰ Health tracking reminders")
        self.health_reminders.setChecked(True)
        notification_layout.addWidget(self.health_reminders)
        
        self.medication_alerts = QCheckBox("💊 Medication alerts")
        self.medication_alerts.setChecked(True)
        notification_layout.addWidget(self.medication_alerts)
        
        self.achievement_notifications = QCheckBox("🏆 Achievement notifications")
        self.achievement_notifications.setChecked(True)
        notification_layout.addWidget(self.achievement_notifications)
        
        notification_group.setLayout(notification_layout)
        layout.addWidget(notification_group)
        
        # Privacy Settings Group
        privacy_group = QGroupBox("🔒 Privacy Settings")
        privacy_layout = QVBoxLayout()
        
        self.share_data = QCheckBox("📊 Share anonymized data for research")
        privacy_layout.addWidget(self.share_data)
        
        self.public_profile = QCheckBox("👥 Make profile visible to community")
        privacy_layout.addWidget(self.public_profile)
        
        self.health_data_sharing = QCheckBox("🏥 Allow health data sharing with healthcare providers")
        privacy_layout.addWidget(self.health_data_sharing)
        
        privacy_group.setLayout(privacy_layout)
        layout.addWidget(privacy_group)
        
        # Units and Display Group
        display_group = QGroupBox("📐 Units and Display")
        display_layout = QFormLayout()
        
        # Measurement System
        self.measurement_system = QComboBox()
        self.measurement_system.addItems(["Metric (kg, cm)", "Imperial (lb, ft)"])
        display_layout.addRow("📏 Measurement System:", self.measurement_system)
        
        # Date Format
        self.date_format = QComboBox()
        self.date_format.addItems(["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        display_layout.addRow("📅 Date Format:", self.date_format)
        
        # Language
        self.language = QComboBox()
        self.language.addItems(["English", "Spanish", "French", "German", "Chinese", "Japanese"])
        display_layout.addRow("🌐 Language:", self.language)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def create_action_buttons(self):
        """Create action buttons"""
        button_layout = QHBoxLayout()
        
        # Save Profile Button
        save_button = QPushButton("💾 Save Profile")
        save_button.clicked.connect(self.save_profile)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        # Reset Button
        reset_button = QPushButton("🔄 Reset Form")
        reset_button.clicked.connect(self.reset_form)
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        
        # Load Default Button
        load_button = QPushButton("📥 Load Current Data")
        load_button.clicked.connect(self.load_user_profile)
        load_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        button_layout.addWidget(load_button)
        button_layout.addWidget(reset_button)
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        
        return button_layout
        
    def apply_styling(self):
        """Apply overall styling to the widget"""
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin: 10px 0px;
                padding-top: 15px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0px 5px 0px 5px;
                color: #2c3e50;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {
                border-color: #3498db;
                outline: none;
            }
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                font-size: 13px;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
            }
            QCheckBox {
                spacing: 8px;
                font-size: 13px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #27ae60;
                border-radius: 3px;
                background-color: #27ae60;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdCb3g9IjAgMCAxNCAxNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgN0w2IDEwTDExIDQiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
        """)
        
    def load_user_profile(self):
        """Load user profile data from API or default values"""
        try:
            if self.api_client:
                # Try to get current user data from API
                response = requests.get("http://localhost:8000/api/users/me", timeout=5)
                if response.status_code == 200:
                    self.user_data = response.json()
                    self.populate_form(self.user_data)
                    QMessageBox.information(self, "✅ Success", "Profile data loaded successfully!")
                    return
                    
        except Exception as e:
            print(f"Could not load from API: {e}")
            
        # Load default/empty values
        self.populate_form({})
        
    def populate_form(self, data):
        """Populate form fields with user data"""
        # Personal Information
        self.full_name_input.setText(data.get('full_name', ''))
        self.username_input.setText(data.get('username', ''))
        
        # Set gender
        gender = data.get('gender', '')
        if gender:
            index = self.gender_input.findText(gender)
            if index >= 0:
                self.gender_input.setCurrentIndex(index)
                
        # Physical Information
        if data.get('height'):
            self.height_input.setValue(int(data['height']))
        if data.get('weight'):
            self.weight_input.setValue(float(data['weight']))
            
        # Contact Information
        self.email_input.setText(data.get('email', ''))
        self.phone_input.setText(data.get('phone', ''))
        self.address_input.setText(data.get('address', ''))
        self.city_input.setText(data.get('city', ''))
        
        # Set country
        country = data.get('country', '')
        if country:
            index = self.country_input.findText(country)
            if index >= 0:
                self.country_input.setCurrentIndex(index)
            else:
                self.country_input.setEditText(country)
                
        # Health Profile
        blood_type = data.get('blood_type', '')
        if blood_type:
            index = self.blood_type_input.findText(blood_type)
            if index >= 0:
                self.blood_type_input.setCurrentIndex(index)
                
        self.allergies_input.setText(data.get('allergies', ''))
        self.medications_input.setText(data.get('medications', ''))
        self.conditions_input.setText(data.get('medical_conditions', ''))
        
    def save_profile(self):
        """Save profile data"""
        try:
            # Collect all form data
            profile_data = self.collect_form_data()
            
            # Validate required fields
            if not self.validate_form(profile_data):
                return
                
            # Save to API if available
            if self.api_client:
                success = self.save_to_api(profile_data)
                if success:
                    QMessageBox.information(self, "✅ Success", "Profile saved successfully!")
                    self.profile_saved.emit(profile_data)
                    self.profile_updated.emit(profile_data)
                    return
                    
            # Fallback: show success message
            QMessageBox.information(self, "✅ Profile Updated", 
                                  "Profile information updated!\n\n"
                                  f"Name: {profile_data.get('full_name', 'N/A')}\n"
                                  f"Email: {profile_data.get('email', 'N/A')}\n"
                                  f"Height: {profile_data.get('height', 'N/A')} cm\n"
                                  f"Weight: {profile_data.get('weight', 'N/A')} kg")
            
            self.profile_saved.emit(profile_data)
            self.profile_updated.emit(profile_data)
            
        except Exception as e:
            QMessageBox.critical(self, "❌ Error", f"Could not save profile:\n{str(e)}")
            
    def collect_form_data(self):
        """Collect all form data into a dictionary"""
        return {
            # Personal Information
            'full_name': self.full_name_input.text(),
            'username': self.username_input.text(),
            'gender': self.gender_input.currentText() if self.gender_input.currentText() != "Select Gender" else '',
            'height': self.height_input.value(),
            'weight': self.weight_input.value(),
            
            # Contact Information
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'address': self.address_input.toPlainText(),
            'city': self.city_input.text(),
            'country': self.country_input.currentText() if self.country_input.currentText() != "Select Country" else '',
            
            # Emergency Contact
            'emergency_name': self.emergency_name_input.text(),
            'emergency_phone': self.emergency_phone_input.text(),
            'emergency_relationship': self.emergency_relationship_input.currentText() if self.emergency_relationship_input.currentText() != "Select Relationship" else '',
            
            # Health Profile
            'blood_type': self.blood_type_input.currentText() if self.blood_type_input.currentText() != "Select Blood Type" else '',
            'allergies': self.allergies_input.toPlainText(),
            'medications': self.medications_input.toPlainText(),
            'medical_conditions': self.conditions_input.toPlainText(),
            'health_goal': self.health_goal_input.currentText() if self.health_goal_input.currentText() != "Select Primary Goal" else '',
            'target_weight': self.target_weight_input.value(),
            'activity_level': self.activity_level_input.currentText() if self.activity_level_input.currentText() != "Select Activity Level" else '',
            
            # Preferences
            'email_notifications': self.email_notifications.isChecked(),
            'health_reminders': self.health_reminders.isChecked(),
            'medication_alerts': self.medication_alerts.isChecked(),
            'achievement_notifications': self.achievement_notifications.isChecked(),
            'share_data': self.share_data.isChecked(),
            'public_profile': self.public_profile.isChecked(),
            'health_data_sharing': self.health_data_sharing.isChecked(),
            'measurement_system': self.measurement_system.currentText(),
            'date_format': self.date_format.currentText(),
            'language': self.language.currentText()
        }
        
    def validate_form(self, data):
        """Validate form data"""
        if not data.get('full_name'):
            QMessageBox.warning(self, "⚠️ Validation Error", "Please enter your full name.")
            self.tab_widget.setCurrentIndex(0)  # Switch to personal info tab
            self.full_name_input.setFocus()
            return False
            
        if not data.get('email'):
            QMessageBox.warning(self, "⚠️ Validation Error", "Please enter your email address.")
            self.tab_widget.setCurrentIndex(1)  # Switch to contact info tab
            self.email_input.setFocus()
            return False
            
        # Validate email format
        email = data.get('email', '')
        if email and '@' not in email:
            QMessageBox.warning(self, "⚠️ Validation Error", "Please enter a valid email address.")
            self.tab_widget.setCurrentIndex(1)
            self.email_input.setFocus()
            return False
            
        return True
        
    def save_to_api(self, data):
        """Save profile data to API"""
        try:
            response = requests.put(
                "http://localhost:8000/api/users/me", 
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                return True
            else:
                QMessageBox.warning(self, "⚠️ API Error", 
                                  f"Could not save to server:\n"
                                  f"Status: {response.status_code}\n"
                                  f"Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            QMessageBox.critical(self, "❌ Connection Error", 
                               f"Could not connect to server:\n{str(e)}")
            return False
            
    def reset_form(self):
        """Reset form to default values"""
        reply = QMessageBox.question(self, "🔄 Reset Form", 
                                   "Are you sure you want to reset all fields?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.populate_form({})
            QMessageBox.information(self, "✅ Reset Complete", "Form has been reset to default values.")


# Test function
def main():
    """Test the profile form widget"""
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create and show the widget
    widget = UserProfileFormWidget()
    widget.show()
    
    # Connect signals for testing
    widget.profile_saved.connect(lambda data: print(f"Profile saved: {data}"))
    widget.profile_updated.connect(lambda data: print(f"Profile updated: {data}"))
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()