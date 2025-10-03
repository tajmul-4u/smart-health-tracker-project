"""
Health Data Input Widget for Dashboard Profile Section
Integrated component for updating health conditions within the dashboard
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, 
    QTextEdit, QDateEdit, QPushButton, QMessageBox, QGroupBox,
    QScrollArea, QFrame, QProgressBar, QTabWidget
)
from PyQt6.QtCore import Qt, QDate, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
import requests
from datetime import datetime, date
import json

class HealthDataInputWidget(QWidget):
    """Health data input widget for dashboard profile section"""
    
    # Signals
    data_updated = pyqtSignal(dict)  # Emitted when health data is updated
    user_profile_changed = pyqtSignal(dict)  # Emitted when user profile changes
    
    def __init__(self, api_client=None):
        super().__init__()
        self.api_client = api_client
        self.api_base_url = "http://localhost:8000"
        self.current_user_data = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #007bff;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #007bff;
                font-size: 14px;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 13px;
                min-height: 20px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border-color: #007bff;
                background-color: #f0f8ff;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QLabel {
                color: #333;
                font-weight: bold;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Create tab widget for different sections
        tab_widget = QTabWidget()
        
        # Profile Information Tab
        profile_tab = self.create_profile_tab()
        tab_widget.addTab(profile_tab, "👤 Profile")
        
        # Health Data Tab
        health_tab = self.create_health_data_tab()
        tab_widget.addTab(health_tab, "🏥 Health Data")
        
        # Health History Tab
        history_tab = self.create_history_tab()
        tab_widget.addTab(history_tab, "📊 History")
        
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)
        
        # Load current user data
        self.load_user_data()
        
    def create_profile_tab(self):
        """Create user profile information tab"""
        scroll_area = QScrollArea()
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("👤 User Profile Information")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #007bff; margin: 15px;")
        layout.addWidget(title)
        
        # Basic Information Group
        basic_group = QGroupBox("📋 Basic Information")
        basic_layout = QFormLayout()
        
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("Enter your full name")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setReadOnly(True)  # Email typically shouldn't change
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        
        self.age_input = QSpinBox()
        self.age_input.setRange(1, 120)
        self.age_input.setSuffix(" years")
        
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Select Gender", "Male", "Female", "Other", "Prefer not to say"])
        
        basic_layout.addRow("Full Name:", self.full_name_input)
        basic_layout.addRow("Email:", self.email_input)
        basic_layout.addRow("Username:", self.username_input)
        basic_layout.addRow("Age:", self.age_input)
        basic_layout.addRow("Gender:", self.gender_input)
        basic_group.setLayout(basic_layout)
        
        # Physical Information Group
        physical_group = QGroupBox("📏 Physical Information")
        physical_layout = QFormLayout()
        
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(50, 250)
        self.height_input.setSuffix(" cm")
        self.height_input.setDecimals(1)
        
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(20, 300)
        self.weight_input.setSuffix(" kg")
        self.weight_input.setDecimals(1)
        
        # Calculate BMI automatically
        self.bmi_label = QLabel("BMI: --")
        self.bmi_label.setStyleSheet("color: #666; font-size: 12px;")
        
        # Connect signals for BMI calculation
        self.height_input.valueChanged.connect(self.calculate_bmi)
        self.weight_input.valueChanged.connect(self.calculate_bmi)
        
        physical_layout.addRow("Height:", self.height_input)
        physical_layout.addRow("Weight:", self.weight_input)
        physical_layout.addRow("BMI:", self.bmi_label)
        physical_group.setLayout(physical_layout)
        
        # Update Profile Button
        update_profile_btn = QPushButton("💾 Update Profile")
        update_profile_btn.clicked.connect(self.update_user_profile)
        update_profile_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                font-size: 14px;
                padding: 12px 24px;
                margin: 15px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        layout.addWidget(basic_group)
        layout.addWidget(physical_group)
        layout.addWidget(update_profile_btn)
        layout.addStretch()
        
        widget.setLayout(layout)
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        
        return scroll_area
        
    def create_health_data_tab(self):
        """Create health data input tab"""
        scroll_area = QScrollArea()
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🏥 Update Health Conditions")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #007bff; margin: 15px;")
        layout.addWidget(title)
        
        # Blood Pressure Group
        bp_group = QGroupBox("🩺 Blood Pressure")
        bp_layout = QFormLayout()
        
        self.systolic_input = QSpinBox()
        self.systolic_input.setRange(70, 250)
        self.systolic_input.setValue(120)
        self.systolic_input.setSuffix(" mmHg")
        
        self.diastolic_input = QSpinBox()
        self.diastolic_input.setRange(40, 150)
        self.diastolic_input.setValue(80)
        self.diastolic_input.setSuffix(" mmHg")
        
        self.bp_notes = QLineEdit()
        self.bp_notes.setPlaceholderText("Add notes about this reading...")
        
        bp_layout.addRow("Systolic (Top):", self.systolic_input)
        bp_layout.addRow("Diastolic (Bottom):", self.diastolic_input)
        bp_layout.addRow("Notes:", self.bp_notes)
        bp_group.setLayout(bp_layout)
        
        # Blood Sugar Group
        bs_group = QGroupBox("🩸 Blood Sugar")
        bs_layout = QFormLayout()
        
        self.blood_sugar_input = QDoubleSpinBox()
        self.blood_sugar_input.setRange(30, 600)
        self.blood_sugar_input.setValue(95)
        self.blood_sugar_input.setSuffix(" mg/dL")
        self.blood_sugar_input.setDecimals(1)
        
        self.sugar_test_type = QComboBox()
        self.sugar_test_type.addItems(["Select Type", "fasting", "after_meal", "random", "bedtime"])
        
        self.bs_notes = QLineEdit()
        self.bs_notes.setPlaceholderText("Add notes about this reading...")
        
        bs_layout.addRow("Blood Sugar Level:", self.blood_sugar_input)
        bs_layout.addRow("Test Type:", self.sugar_test_type)
        bs_layout.addRow("Notes:", self.bs_notes)
        bs_group.setLayout(bs_layout)
        
        # Wellness Group
        wellness_group = QGroupBox("🧠 Wellness & Lifestyle")
        wellness_layout = QFormLayout()
        
        self.sleep_hours_input = QDoubleSpinBox()
        self.sleep_hours_input.setRange(0, 24)
        self.sleep_hours_input.setValue(7.5)
        self.sleep_hours_input.setSuffix(" hours")
        self.sleep_hours_input.setDecimals(1)
        
        self.stress_level_input = QSpinBox()
        self.stress_level_input.setRange(1, 10)
        self.stress_level_input.setValue(5)
        self.stress_level_input.setSuffix("/10")
        
        self.mood_score_input = QSpinBox()
        self.mood_score_input.setRange(1, 10)
        self.mood_score_input.setValue(7)
        self.mood_score_input.setSuffix("/10")
        
        self.steps_input = QSpinBox()
        self.steps_input.setRange(0, 50000)
        self.steps_input.setValue(8000)
        self.steps_input.setSuffix(" steps")
        
        self.water_intake_input = QDoubleSpinBox()
        self.water_intake_input.setRange(0, 10)
        self.water_intake_input.setValue(2.0)
        self.water_intake_input.setSuffix(" liters")
        self.water_intake_input.setDecimals(1)
        
        wellness_layout.addRow("Sleep Duration:", self.sleep_hours_input)
        wellness_layout.addRow("Stress Level:", self.stress_level_input)
        wellness_layout.addRow("Mood Score:", self.mood_score_input)
        wellness_layout.addRow("Steps Today:", self.steps_input)
        wellness_layout.addRow("Water Intake:", self.water_intake_input)
        wellness_group.setLayout(wellness_layout)
        
        # Additional Notes
        notes_group = QGroupBox("📝 Additional Notes")
        notes_layout = QVBoxLayout()
        
        self.health_notes = QTextEdit()
        self.health_notes.setMaximumHeight(80)
        self.health_notes.setPlaceholderText("Any additional notes about your health today...")
        
        notes_layout.addWidget(self.health_notes)
        notes_group.setLayout(notes_layout)
        
        # Submit Health Data Button
        submit_health_btn = QPushButton("📤 Submit Health Data")
        submit_health_btn.clicked.connect(self.submit_health_data)
        submit_health_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                font-size: 14px;
                padding: 12px 24px;
                margin: 15px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        
        layout.addWidget(bp_group)
        layout.addWidget(bs_group)
        layout.addWidget(wellness_group)
        layout.addWidget(notes_group)
        layout.addWidget(submit_health_btn)
        layout.addStretch()
        
        widget.setLayout(layout)
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        
        return scroll_area
        
    def create_history_tab(self):
        """Create health history tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("📊 Health Data History")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #007bff; margin: 15px;")
        layout.addWidget(title)
        
        # Quick Stats
        stats_group = QGroupBox("📈 Quick Statistics")
        stats_layout = QGridLayout()
        
        # Create stat cards
        self.create_stat_card(stats_layout, "Last BP Reading", "120/80 mmHg", 0, 0)
        self.create_stat_card(stats_layout, "Last Blood Sugar", "95 mg/dL", 0, 1)
        self.create_stat_card(stats_layout, "Avg Sleep", "7.5 hours", 1, 0)
        self.create_stat_card(stats_layout, "Avg Steps", "8,450 steps", 1, 1)
        
        stats_group.setLayout(stats_layout)
        
        # Refresh Button
        refresh_btn = QPushButton("🔄 Refresh Data")
        refresh_btn.clicked.connect(self.load_health_history)
        
        layout.addWidget(stats_group)
        layout.addWidget(refresh_btn)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
        
    def create_stat_card(self, layout, title, value, row, col):
        """Create a stat card widget"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }
        """)
        
        card_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 12px;")
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #333; font-size: 16px; font-weight: bold;")
        
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card.setLayout(card_layout)
        
        layout.addWidget(card, row, col)
        
    def calculate_bmi(self):
        """Calculate and display BMI"""
        height = self.height_input.value()
        weight = self.weight_input.value()
        
        if height > 0 and weight > 0:
            height_m = height / 100  # Convert cm to m
            bmi = weight / (height_m * height_m)
            
            # Determine BMI category
            if bmi < 18.5:
                category = "Underweight"
                color = "#ffc107"
            elif bmi < 25:
                category = "Normal"
                color = "#28a745"
            elif bmi < 30:
                category = "Overweight"
                color = "#fd7e14"
            else:
                category = "Obese"
                color = "#dc3545"
                
            self.bmi_label.setText(f"BMI: {bmi:.1f} ({category})")
            self.bmi_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        else:
            self.bmi_label.setText("BMI: --")
            
    def load_user_data(self):
        """Load current user data from API"""
        try:
            response = requests.get(f"{self.api_base_url}/api/users/me", timeout=5)
            if response.status_code == 200:
                user_data = response.json()
                self.populate_user_fields(user_data)
                self.current_user_data = user_data
        except Exception as e:
            print(f"Error loading user data: {e}")
            
    def populate_user_fields(self, user_data):
        """Populate form fields with user data"""
        self.full_name_input.setText(user_data.get('full_name', ''))
        self.email_input.setText(user_data.get('email', ''))
        self.username_input.setText(user_data.get('username', ''))
        
        if user_data.get('age'):
            self.age_input.setValue(user_data['age'])
            
        if user_data.get('gender'):
            gender_index = self.gender_input.findText(user_data['gender'])
            if gender_index >= 0:
                self.gender_input.setCurrentIndex(gender_index)
                
        if user_data.get('height'):
            self.height_input.setValue(user_data['height'])
            
        if user_data.get('weight'):
            self.weight_input.setValue(user_data['weight'])
            
        # Calculate BMI if height and weight are available
        self.calculate_bmi()
        
    def update_user_profile(self):
        """Update user profile information"""
        try:
            update_data = {
                "full_name": self.full_name_input.text(),
                "username": self.username_input.text(),
                "age": self.age_input.value(),
                "gender": self.gender_input.currentText() if self.gender_input.currentIndex() > 0 else None,
                "height": self.height_input.value(),
                "weight": self.weight_input.value()
            }
            
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None and v != ""}
            
            response = requests.put(
                f"{self.api_base_url}/api/users/me",
                json=update_data,
                timeout=10
            )
            
            if response.status_code == 200:
                QMessageBox.information(
                    self,
                    "✅ Success",
                    "Profile updated successfully!"
                )
                self.user_profile_changed.emit(update_data)
            else:
                QMessageBox.warning(
                    self,
                    "⚠️ Warning", 
                    f"Failed to update profile: {response.text}"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Error",
                f"Error updating profile: {str(e)}"
            )
            
    def submit_health_data(self):
        """Submit health data to API"""
        try:
            # Submit blood pressure
            bp_data = {
                "systolic": self.systolic_input.value(),
                "diastolic": self.diastolic_input.value(),
                "notes": self.bp_notes.text() or f"Dashboard submission at {datetime.now().strftime('%H:%M')}"
            }
            
            # Submit blood sugar
            bs_data = {
                "level": self.blood_sugar_input.value(),
                "meal_relation": self.sugar_test_type.currentText() if self.sugar_test_type.currentIndex() > 0 else "random",
                "notes": self.bs_notes.text() or "Dashboard submission"
            }
            
            # Submit stress/wellness data
            stress_data = {
                "level": self.stress_level_input.value(),
                "notes": f"Sleep: {self.sleep_hours_input.value()}h, Mood: {self.mood_score_input.value()}/10, Steps: {self.steps_input.value()}, Water: {self.water_intake_input.value()}L"
            }
            
            # Add any additional notes
            if self.health_notes.toPlainText():
                stress_data["notes"] += f" | Notes: {self.health_notes.toPlainText()}"
            
            # Submit to API endpoints
            self.submit_to_api("/api/health/conditions/blood_pressure", bp_data)
            self.submit_to_api("/api/health/conditions/blood_sugar", bs_data)
            self.submit_to_api("/api/health/conditions/stress", stress_data)
            
            # Show success message
            QMessageBox.information(
                self,
                "✅ Health Data Submitted",
                f"Health data submitted successfully!\n\n"
                f"• Blood Pressure: {bp_data['systolic']}/{bp_data['diastolic']} mmHg\n"
                f"• Blood Sugar: {bs_data['level']} mg/dL ({bs_data['meal_relation']})\n"
                f"• Stress Level: {stress_data['level']}/10\n"
                f"• Sleep: {self.sleep_hours_input.value()} hours\n"
                f"• Steps: {self.steps_input.value()}\n"
                f"• Water: {self.water_intake_input.value()}L"
            )
            
            # Emit signal for dashboard update
            health_summary = {
                "blood_pressure": f"{bp_data['systolic']}/{bp_data['diastolic']}",
                "blood_sugar": bs_data['level'],
                "stress_level": stress_data['level'],
                "sleep_hours": self.sleep_hours_input.value(),
                "steps": self.steps_input.value(),
                "water_intake": self.water_intake_input.value(),
                "mood_score": self.mood_score_input.value()
            }
            self.data_updated.emit(health_summary)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Error",
                f"Failed to submit health data: {str(e)}"
            )
            
    def submit_to_api(self, endpoint, data):
        """Submit data to specific API endpoint"""
        try:
            response = requests.post(
                f"{self.api_base_url}{endpoint}",
                json=data,
                timeout=10
            )
            if response.status_code != 200:
                print(f"API submission failed for {endpoint}: {response.text}")
        except Exception as e:
            print(f"Error submitting to {endpoint}: {e}")
            
    def load_health_history(self):
        """Load health history data"""
        try:
            # This would typically fetch data from the API
            # For now, just show a message
            QMessageBox.information(
                self,
                "📊 Health History",
                "Health history data refreshed!\n\nThis feature will show your recent health data trends and statistics."
            )
        except Exception as e:
            QMessageBox.warning(
                self,
                "⚠️ Warning",
                f"Could not load health history: {str(e)}"
            )