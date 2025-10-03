#!/usr/bin/env python3
"""
Simple Health Data Input Form - Easy to use interface for health data entry
"""

import sys
import requests
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QFormLayout, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QTextEdit, QPushButton, QMessageBox, QGroupBox,
    QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class SimpleHealthForm(QMainWindow):
    """Simple and clear health data input form"""
    
    def __init__(self):
        super().__init__()
        self.api_base_url = "http://localhost:8000"
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🏥 Health Tracker - Data Input")
        self.setGeometry(200, 100, 600, 800)
        
        # Set style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 12px;
                color: #333;
                font-weight: bold;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
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
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
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
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create scroll area for the form
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("🏥 Health Data Entry Form")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #007bff; margin: 20px; font-size: 20px;")
        main_layout.addWidget(title_label)
        
        # Instruction
        instruction_label = QLabel("Fill in your health data below and click 'Submit Data' to save:")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setStyleSheet("color: #666; margin-bottom: 20px; font-size: 14px;")
        main_layout.addWidget(instruction_label)
        
        # Create form sections
        self.create_form_sections(main_layout)
        
        # Submit button
        submit_button = QPushButton("📤 Submit Health Data")
        submit_button.clicked.connect(self.submit_data)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                font-size: 16px;
                padding: 15px 30px;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        main_layout.addWidget(submit_button)
        
        # Clear button
        clear_button = QPushButton("🗑️ Clear Form")
        clear_button.clicked.connect(self.clear_form)
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                font-size: 14px;
                padding: 10px 20px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        main_layout.addWidget(clear_button)
        
        # Set up scroll area
        scroll_widget.setLayout(main_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        # Final layout
        final_layout = QVBoxLayout()
        final_layout.addWidget(scroll_area)
        central_widget.setLayout(final_layout)
        
    def create_form_sections(self, main_layout):
        """Create all form sections with input fields"""
        
        # Blood Pressure Section
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
        
        bp_layout.addRow("Systolic (Top Number):", self.systolic_input)
        bp_layout.addRow("Diastolic (Bottom Number):", self.diastolic_input)
        bp_group.setLayout(bp_layout)
        main_layout.addWidget(bp_group)
        
        # Blood Sugar Section
        bs_group = QGroupBox("🩸 Blood Sugar")
        bs_layout = QFormLayout()
        
        self.blood_sugar_input = QDoubleSpinBox()
        self.blood_sugar_input.setRange(30, 600)
        self.blood_sugar_input.setValue(95)
        self.blood_sugar_input.setSuffix(" mg/dL")
        self.blood_sugar_input.setDecimals(1)
        
        self.sugar_test_type = QComboBox()
        self.sugar_test_type.addItems(["Select Type", "fasting", "after_meal", "random"])
        
        bs_layout.addRow("Blood Sugar Level:", self.blood_sugar_input)
        bs_layout.addRow("Test Type:", self.sugar_test_type)
        bs_group.setLayout(bs_layout)
        main_layout.addWidget(bs_group)
        
        # Sleep Section
        sleep_group = QGroupBox("😴 Sleep & Rest")
        sleep_layout = QFormLayout()
        
        self.sleep_hours_input = QDoubleSpinBox()
        self.sleep_hours_input.setRange(0, 24)
        self.sleep_hours_input.setValue(7.5)
        self.sleep_hours_input.setSuffix(" hours")
        self.sleep_hours_input.setDecimals(1)
        
        self.sleep_quality_input = QSpinBox()
        self.sleep_quality_input.setRange(1, 10)
        self.sleep_quality_input.setValue(7)
        self.sleep_quality_input.setSuffix("/10")
        
        sleep_layout.addRow("Sleep Duration:", self.sleep_hours_input)
        sleep_layout.addRow("Sleep Quality (1-10):", self.sleep_quality_input)
        sleep_group.setLayout(sleep_layout)
        main_layout.addWidget(sleep_group)
        
        # Physical Activity Section
        activity_group = QGroupBox("🏃 Physical Activity")
        activity_layout = QFormLayout()
        
        self.steps_input = QSpinBox()
        self.steps_input.setRange(0, 50000)
        self.steps_input.setValue(8000)
        self.steps_input.setSuffix(" steps")
        
        self.exercise_minutes_input = QSpinBox()
        self.exercise_minutes_input.setRange(0, 500)
        self.exercise_minutes_input.setValue(30)
        self.exercise_minutes_input.setSuffix(" minutes")
        
        activity_layout.addRow("Steps Count:", self.steps_input)
        activity_layout.addRow("Exercise Duration:", self.exercise_minutes_input)
        activity_group.setLayout(activity_layout)
        main_layout.addWidget(activity_group)
        
        # Stress & Mood Section
        mood_group = QGroupBox("🧠 Mental Health")
        mood_layout = QFormLayout()
        
        self.stress_level_input = QSpinBox()
        self.stress_level_input.setRange(1, 10)
        self.stress_level_input.setValue(5)
        self.stress_level_input.setSuffix("/10")
        
        self.mood_score_input = QSpinBox()
        self.mood_score_input.setRange(1, 10)
        self.mood_score_input.setValue(7)
        self.mood_score_input.setSuffix("/10")
        
        mood_layout.addRow("Stress Level (1-10):", self.stress_level_input)
        mood_layout.addRow("Mood Score (1-10):", self.mood_score_input)
        mood_group.setLayout(mood_layout)
        main_layout.addWidget(mood_group)
        
        # Additional Metrics Section
        metrics_group = QGroupBox("📊 Additional Metrics")
        metrics_layout = QFormLayout()
        
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(30, 300)
        self.weight_input.setValue(70.0)
        self.weight_input.setSuffix(" kg")
        self.weight_input.setDecimals(1)
        
        self.heart_rate_input = QSpinBox()
        self.heart_rate_input.setRange(40, 200)
        self.heart_rate_input.setValue(72)
        self.heart_rate_input.setSuffix(" bpm")
        
        self.water_intake_input = QDoubleSpinBox()
        self.water_intake_input.setRange(0, 10)
        self.water_intake_input.setValue(2.0)
        self.water_intake_input.setSuffix(" liters")
        self.water_intake_input.setDecimals(1)
        
        metrics_layout.addRow("Weight:", self.weight_input)
        metrics_layout.addRow("Heart Rate:", self.heart_rate_input)
        metrics_layout.addRow("Water Intake:", self.water_intake_input)
        metrics_group.setLayout(metrics_layout)
        main_layout.addWidget(metrics_group)
        
        # Notes Section
        notes_group = QGroupBox("📝 Additional Notes")
        notes_layout = QFormLayout()
        
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        self.notes_input.setPlaceholderText("Enter any additional notes about your health today...")
        
        notes_layout.addRow("Notes:", self.notes_input)
        notes_group.setLayout(notes_layout)
        main_layout.addWidget(notes_group)
        
    def clear_form(self):
        """Clear all form fields"""
        self.systolic_input.setValue(120)
        self.diastolic_input.setValue(80)
        self.blood_sugar_input.setValue(95)
        self.sugar_test_type.setCurrentIndex(0)
        self.sleep_hours_input.setValue(7.5)
        self.sleep_quality_input.setValue(7)
        self.steps_input.setValue(8000)
        self.exercise_minutes_input.setValue(30)
        self.stress_level_input.setValue(5)
        self.mood_score_input.setValue(7)
        self.weight_input.setValue(70.0)
        self.heart_rate_input.setValue(72)
        self.water_intake_input.setValue(2.0)
        self.notes_input.clear()
        
        QMessageBox.information(self, "Form Cleared", "All fields have been reset to default values.")
        
    def submit_data(self):
        """Submit the health data to the API"""
        try:
            # Collect all data
            health_data = {
                "blood_pressure": {
                    "systolic": self.systolic_input.value(),
                    "diastolic": self.diastolic_input.value(),
                    "notes": f"Submitted via GUI at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                },
                "blood_sugar": {
                    "level": self.blood_sugar_input.value(),
                    "meal_relation": self.sugar_test_type.currentText() if self.sugar_test_type.currentIndex() > 0 else "random",
                    "notes": "GUI submission"
                },
                "physical_activity": {
                    "steps": self.steps_input.value(),
                    "exercise_minutes": self.exercise_minutes_input.value()
                },
                "wellness": {
                    "sleep_hours": self.sleep_hours_input.value(),
                    "sleep_quality": self.sleep_quality_input.value(),
                    "stress_level": self.stress_level_input.value(),
                    "mood_score": self.mood_score_input.value()
                },
                "metrics": {
                    "weight": self.weight_input.value(),
                    "heart_rate": self.heart_rate_input.value(),
                    "water_intake": self.water_intake_input.value()
                },
                "notes": self.notes_input.toPlainText()
            }
            
            # Submit each data type to separate endpoints
            self.submit_blood_pressure(health_data["blood_pressure"])
            self.submit_blood_sugar(health_data["blood_sugar"])
            self.submit_stress_data(health_data["wellness"])
            
            # Show success message
            QMessageBox.information(
                self, 
                "✅ Success", 
                "Health data submitted successfully!\n\n"
                f"• Blood Pressure: {health_data['blood_pressure']['systolic']}/{health_data['blood_pressure']['diastolic']} mmHg\n"
                f"• Blood Sugar: {health_data['blood_sugar']['level']} mg/dL\n"
                f"• Sleep: {health_data['wellness']['sleep_hours']} hours\n"
                f"• Steps: {health_data['physical_activity']['steps']}\n"
                f"• Mood: {health_data['wellness']['mood_score']}/10"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "❌ Error", f"Failed to submit data:\n{str(e)}")
    
    def submit_blood_pressure(self, data):
        """Submit blood pressure data"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/health/conditions/blood_pressure",
                json=data,
                timeout=10
            )
            if response.status_code != 200:
                print(f"Blood pressure submission failed: {response.text}")
        except Exception as e:
            print(f"Blood pressure submission error: {e}")
    
    def submit_blood_sugar(self, data):
        """Submit blood sugar data"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/health/conditions/blood_sugar",
                json=data,
                timeout=10
            )
            if response.status_code != 200:
                print(f"Blood sugar submission failed: {response.text}")
        except Exception as e:
            print(f"Blood sugar submission error: {e}")
    
    def submit_stress_data(self, data):
        """Submit stress/wellness data"""
        try:
            stress_data = {
                "level": data["stress_level"],
                "notes": f"Sleep: {data['sleep_hours']}h, Quality: {data['sleep_quality']}/10, Mood: {data['mood_score']}/10"
            }
            response = requests.post(
                f"{self.api_base_url}/api/health/conditions/stress",
                json=stress_data,
                timeout=10
            )
            if response.status_code != 200:
                print(f"Stress data submission failed: {response.text}")
        except Exception as e:
            print(f"Stress data submission error: {e}")

def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Health Tracker")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Smart Health Tracker")
    
    # Create and show the main window
    window = SimpleHealthForm()
    window.show()
    
    # Start the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()