#!/usr/bin/env python3
"""
Simple Health Data Input Widget - No QtCharts dependency
A lightweight health data input form for the Smart Health Tracker
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, 
    QTextEdit, QDateTimeEdit, QPushButton, QMessageBox, QGroupBox,
    QScrollArea, QFrame, QProgressBar, QTabWidget, QSlider,
    QCheckBox, QApplication, QDialog
)
from PyQt6.QtCore import Qt, QDateTime, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor, QLinearGradient
import requests
from datetime import datetime, date, timedelta
import json

class SimpleHealthDataInput(QWidget):
    """Simple health data input system without charts dependency"""
    
    # Signals
    data_submitted = pyqtSignal(dict)
    data_updated = pyqtSignal(dict)
    validation_failed = pyqtSignal(str)
    
    def __init__(self, api_client=None):
        super().__init__()
        self.api_client = api_client
        self.api_base_url = "http://localhost:8000"
        self.current_data = {}
        
        self.init_ui()
        self.setup_validation()
        
    def init_ui(self):
        """Initialize simple user interface"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
                color: #007bff;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0056b3, stop:1 #004494);
            }
            QPushButton:pressed {
                background: #004494;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 8px;
                border: 2px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border-color: #007bff;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("🏥 Health Data Input")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header.setStyleSheet("color: #007bff; margin-bottom: 20px;")
        main_layout.addWidget(header)
        
        # Scroll area for form
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        form_widget = QWidget()
        form_layout = QVBoxLayout()
        
        # Vital Signs Group
        vitals_group = self.create_vitals_group()
        form_layout.addWidget(vitals_group)
        
        # Physical Measurements Group
        physical_group = self.create_physical_group()
        form_layout.addWidget(physical_group)
        
        # Lifestyle Group
        lifestyle_group = self.create_lifestyle_group()
        form_layout.addWidget(lifestyle_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Save Data")
        self.save_btn.clicked.connect(self.save_data)
        
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.clicked.connect(self.reset_form)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #545b62);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #545b62, stop:1 #495057);
            }
        """)
        
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        
        form_layout.addLayout(button_layout)
        
        form_widget.setLayout(form_layout)
        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)
        
        # Status bar
        self.status_label = QLabel("✅ Ready to input health data")
        self.status_label.setStyleSheet("color: #28a745; padding: 10px; font-weight: bold;")
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
        
    def create_vitals_group(self):
        """Create vital signs input group"""
        group = QGroupBox("🫀 Vital Signs")
        layout = QFormLayout()
        
        # Blood Pressure
        bp_layout = QHBoxLayout()
        self.systolic_input = QSpinBox()
        self.systolic_input.setRange(70, 250)
        self.systolic_input.setValue(120)
        self.systolic_input.setSuffix(" mmHg")
        
        self.diastolic_input = QSpinBox()
        self.diastolic_input.setRange(40, 150)
        self.diastolic_input.setValue(80)
        self.diastolic_input.setSuffix(" mmHg")
        
        bp_layout.addWidget(QLabel("Systolic:"))
        bp_layout.addWidget(self.systolic_input)
        bp_layout.addWidget(QLabel("Diastolic:"))
        bp_layout.addWidget(self.diastolic_input)
        bp_layout.addStretch()
        
        layout.addRow("🩸 Blood Pressure:", bp_layout)
        
        # Heart Rate
        self.heart_rate_input = QSpinBox()
        self.heart_rate_input.setRange(40, 200)
        self.heart_rate_input.setValue(70)
        self.heart_rate_input.setSuffix(" bpm")
        layout.addRow("💓 Heart Rate:", self.heart_rate_input)
        
        # Temperature
        self.temperature_input = QDoubleSpinBox()
        self.temperature_input.setRange(35.0, 42.0)
        self.temperature_input.setValue(36.5)
        self.temperature_input.setSuffix(" °C")
        self.temperature_input.setDecimals(1)
        layout.addRow("🌡️ Temperature:", self.temperature_input)
        
        # Blood Sugar
        sugar_layout = QHBoxLayout()
        self.blood_sugar_input = QSpinBox()
        self.blood_sugar_input.setRange(50, 500)
        self.blood_sugar_input.setValue(100)
        self.blood_sugar_input.setSuffix(" mg/dL")
        
        self.sugar_test_type = QComboBox()
        self.sugar_test_type.addItems(["Fasting", "Random", "Post-meal", "HbA1c"])
        
        sugar_layout.addWidget(self.blood_sugar_input)
        sugar_layout.addWidget(self.sugar_test_type)
        sugar_layout.addStretch()
        
        layout.addRow("🍬 Blood Sugar:", sugar_layout)
        
        group.setLayout(layout)
        return group
        
    def create_physical_group(self):
        """Create physical measurements group"""
        group = QGroupBox("📏 Physical Measurements")
        layout = QFormLayout()
        
        # Weight
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(30.0, 300.0)
        self.weight_input.setValue(70.0)
        self.weight_input.setSuffix(" kg")
        self.weight_input.setDecimals(1)
        layout.addRow("⚖️ Weight:", self.weight_input)
        
        # Height
        self.height_input = QSpinBox()
        self.height_input.setRange(100, 250)
        self.height_input.setValue(170)
        self.height_input.setSuffix(" cm")
        layout.addRow("📐 Height:", self.height_input)
        
        # BMI (calculated)
        self.bmi_label = QLabel("23.5 (Normal)")
        self.bmi_label.setStyleSheet("font-weight: bold; color: #28a745;")
        layout.addRow("📊 BMI:", self.bmi_label)
        
        # Connect weight/height changes to BMI calculation
        self.weight_input.valueChanged.connect(self.calculate_bmi)
        self.height_input.valueChanged.connect(self.calculate_bmi)
        
        group.setLayout(layout)
        return group
        
    def create_lifestyle_group(self):
        """Create lifestyle input group"""
        group = QGroupBox("🏃 Lifestyle & Activity")
        layout = QFormLayout()
        
        # Sleep
        self.sleep_hours = QDoubleSpinBox()
        self.sleep_hours.setRange(0.0, 24.0)
        self.sleep_hours.setValue(8.0)
        self.sleep_hours.setSuffix(" hours")
        self.sleep_hours.setDecimals(1)
        layout.addRow("😴 Sleep Duration:", self.sleep_hours)
        
        # Exercise
        exercise_layout = QHBoxLayout()
        self.exercise_duration = QSpinBox()
        self.exercise_duration.setRange(0, 300)
        self.exercise_duration.setValue(30)
        self.exercise_duration.setSuffix(" minutes")
        
        self.exercise_type = QComboBox()
        self.exercise_type.addItems([
            "Walking", "Running", "Cycling", "Swimming", 
            "Gym Workout", "Yoga", "Sports", "Other"
        ])
        
        exercise_layout.addWidget(self.exercise_duration)
        exercise_layout.addWidget(self.exercise_type)
        exercise_layout.addStretch()
        
        layout.addRow("🏃 Exercise:", exercise_layout)
        
        # Steps
        self.steps_input = QSpinBox()
        self.steps_input.setRange(0, 50000)
        self.steps_input.setValue(8000)
        self.steps_input.setSuffix(" steps")
        layout.addRow("👟 Daily Steps:", self.steps_input)
        
        # Water intake
        self.water_intake = QDoubleSpinBox()
        self.water_intake.setRange(0.0, 10.0)
        self.water_intake.setValue(2.0)
        self.water_intake.setSuffix(" liters")
        self.water_intake.setDecimals(1)
        layout.addRow("💧 Water Intake:", self.water_intake)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("Any additional notes about your health today...")
        layout.addRow("📝 Notes:", self.notes_input)
        
        group.setLayout(layout)
        return group
    
    def setup_validation(self):
        """Setup validation rules"""
        self.validation_rules = {
            'systolic_bp': {'min': 70, 'max': 250},
            'diastolic_bp': {'min': 40, 'max': 150},
            'blood_sugar': {'min': 50, 'max': 500},
            'heart_rate': {'min': 40, 'max': 200},
            'temperature': {'min': 35.0, 'max': 42.0},
            'weight': {'min': 30, 'max': 300},
            'sleep_hours': {'min': 0, 'max': 24}
        }
    
    def calculate_bmi(self):
        """Calculate and display BMI"""
        weight = self.weight_input.value()
        height = self.height_input.value() / 100  # Convert cm to m
        
        if weight > 0 and height > 0:
            bmi = weight / (height ** 2)
            bmi_category = self.get_bmi_category(bmi)
            color = self.get_bmi_color(bmi)
            
            self.bmi_label.setText(f"{bmi:.1f} ({bmi_category})")
            self.bmi_label.setStyleSheet(f"font-weight: bold; color: {color};")
    
    def get_bmi_category(self, bmi):
        """Get BMI category"""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def get_bmi_color(self, bmi):
        """Get color for BMI category"""
        if bmi < 18.5 or bmi >= 30:
            return "#dc3545"  # Red for underweight/obese
        elif bmi >= 25:
            return "#ffc107"  # Yellow for overweight
        else:
            return "#28a745"  # Green for normal
    
    def collect_data(self):
        """Collect all form data"""
        data = {
            'systolic_bp': self.systolic_input.value(),
            'diastolic_bp': self.diastolic_input.value(),
            'heart_rate': self.heart_rate_input.value(),
            'temperature': self.temperature_input.value(),
            'blood_sugar': self.blood_sugar_input.value(),
            'sugar_test_type': self.sugar_test_type.currentText(),
            'weight': self.weight_input.value(),
            'height': self.height_input.value(),
            'sleep_hours': self.sleep_hours.value(),
            'exercise_duration': self.exercise_duration.value(),
            'exercise_type': self.exercise_type.currentText(),
            'steps': self.steps_input.value(),
            'water_intake': self.water_intake.value(),
            'notes': self.notes_input.toPlainText(),
            'timestamp': datetime.now().isoformat(),
            'bmi': round(self.weight_input.value() / ((self.height_input.value() / 100) ** 2), 1)
        }
        return data
    
    def validate_data(self, data):
        """Validate collected data"""
        errors = []
        
        for field, rules in self.validation_rules.items():
            if field in data:
                value = data[field]
                
                if value < rules['min']:
                    errors.append(f"{field.replace('_', ' ').title()} is too low (minimum: {rules['min']})")
                    
                if value > rules['max']:
                    errors.append(f"{field.replace('_', ' ').title()} is too high (maximum: {rules['max']})")
        
        # Special validation: systolic should be higher than diastolic
        if data.get('systolic_bp', 0) <= data.get('diastolic_bp', 0):
            errors.append("Systolic blood pressure should be higher than diastolic")
                    
        return errors
    
    def save_data(self):
        """Save health data"""
        try:
            data = self.collect_data()
            
            # Validate
            errors = self.validate_data(data)
            if errors:
                error_msg = "Please correct the following:\n\n" + "\n".join(f"• {error}" for error in errors)
                QMessageBox.warning(self, "Validation Error", error_msg)
                self.status_label.setText("❌ Please fix validation errors")
                self.status_label.setStyleSheet("color: #dc3545; padding: 10px; font-weight: bold;")
                return
            
            # Submit data
            self.submit_data(data)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving data: {str(e)}")
            self.status_label.setText("❌ Error saving data")
            self.status_label.setStyleSheet("color: #dc3545; padding: 10px; font-weight: bold;")
    
    def submit_data(self, data):
        """Submit data to API"""
        try:
            if self.api_client:
                response = self.api_client.post("/api/habits", json=data)
            else:
                # Fallback to direct requests
                response = requests.post(f"{self.api_base_url}/api/habits", 
                                       json=data, timeout=5)
            
            if response.status_code in [200, 201]:
                QMessageBox.information(self, "Success", "Health data saved successfully!")
                self.status_label.setText("✅ Data saved successfully")
                self.status_label.setStyleSheet("color: #28a745; padding: 10px; font-weight: bold;")
                self.data_submitted.emit(data)
            else:
                QMessageBox.warning(self, "Warning", f"Server responded with: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            # Save locally if API is not available
            self.save_locally(data)
            QMessageBox.information(self, "Offline Mode", "Data saved locally. Will sync when online.")
            self.status_label.setText("💾 Saved locally (offline)")
            self.status_label.setStyleSheet("color: #ffc107; padding: 10px; font-weight: bold;")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error submitting data: {str(e)}")
    
    def save_locally(self, data):
        """Save data locally"""
        try:
            with open('health_data_local.json', 'a') as f:
                json.dump(data, f)
                f.write('\n')
        except Exception as e:
            print(f"Error saving locally: {e}")
    
    def reset_form(self):
        """Reset form to default values"""
        self.systolic_input.setValue(120)
        self.diastolic_input.setValue(80)
        self.heart_rate_input.setValue(70)
        self.temperature_input.setValue(36.5)
        self.blood_sugar_input.setValue(100)
        self.weight_input.setValue(70.0)
        self.height_input.setValue(170)
        self.sleep_hours.setValue(8.0)
        self.exercise_duration.setValue(30)
        self.steps_input.setValue(8000)
        self.water_intake.setValue(2.0)
        self.notes_input.clear()
        
        self.status_label.setText("🔄 Form reset to defaults")
        self.status_label.setStyleSheet("color: #6c757d; padding: 10px; font-weight: bold;")

def main():
    """Test the simple health input system"""
    app = QApplication([])
    app.setStyleSheet("""
        QApplication {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    """)
    
    # Create main window
    window = QDialog()
    window.setWindowTitle("🏥 Simple Health Data Input")
    window.setGeometry(100, 100, 800, 700)
    
    layout = QVBoxLayout()
    
    # Create the health input widget
    health_input = SimpleHealthDataInput()
    layout.addWidget(health_input)
    
    window.setLayout(layout)
    window.show()
    
    app.exec()

if __name__ == "__main__":
    main()