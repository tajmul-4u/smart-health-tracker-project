import sys
import json
import requests
from datetime import datetime, date
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QFormLayout, QGridLayout, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QTextEdit, QDateTimeEdit, QPushButton, QMessageBox,
    QTabWidget, QScrollArea, QFrame, QSizePolicy, QProgressBar
)
from PyQt5.QtCore import Qt, QDateTime, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QIntValidator, QDoubleValidator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class HealthDataSubmissionThread(QThread):
    """Thread for submitting health data to API"""
    success = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, data, api_url):
        super().__init__()
        self.data = data
        self.api_url = api_url
    
    def run(self):
        try:
            response = requests.post(
                self.api_url,
                json=self.data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                self.success.emit("Health data submitted successfully!")
            else:
                self.error.emit(f"API Error: {response.status_code} - {response.text}")
        
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Network Error: {str(e)}")
        except Exception as e:
            self.error.emit(f"Unexpected Error: {str(e)}")

class HealthDataVisualization(QWidget):
    """Widget for displaying health data charts"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Charts")
        refresh_btn.clicked.connect(self.load_chart_data)
        layout.addWidget(refresh_btn)
        
        self.setLayout(layout)
        self.load_chart_data()
    
    def load_chart_data(self):
        """Load data from API and create charts"""
        try:
            response = requests.get("http://localhost:8000/api/v1/healthdata/charts?days=30", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.create_charts(data)
            else:
                QMessageBox.warning(self, "Warning", f"Could not load chart data: {response.status_code}")
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not load chart data: {str(e)}")
    
    def create_charts(self, data):
        """Create health data charts"""
        self.figure.clear()
        
        # Create subplots
        axes = self.figure.subplots(2, 2)
        
        dates = data.get('dates', [])
        
        # Blood Pressure Chart
        ax1 = axes[0, 0]
        systolic = [v for v in data.get('blood_pressure_systolic', []) if v is not None]
        diastolic = [v for v in data.get('blood_pressure_diastolic', []) if v is not None]
        systolic_dates = [dates[i] for i, v in enumerate(data.get('blood_pressure_systolic', [])) if v is not None]
        
        if systolic:
            ax1.plot(systolic_dates[-len(systolic):], systolic, 'ro-', label='Systolic', linewidth=2)
            ax1.plot(systolic_dates[-len(diastolic):], diastolic, 'bo-', label='Diastolic', linewidth=2)
            ax1.set_title('Blood Pressure Trends')
            ax1.set_ylabel('mmHg')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)
        
        # Weight Chart
        ax2 = axes[0, 1]
        weight = [v for v in data.get('weight', []) if v is not None]
        weight_dates = [dates[i] for i, v in enumerate(data.get('weight', [])) if v is not None]
        
        if weight:
            ax2.plot(weight_dates[-len(weight):], weight, 'go-', linewidth=2)
            ax2.set_title('Weight Trends')
            ax2.set_ylabel('kg')
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(axis='x', rotation=45)
        
        # Sleep Chart
        ax3 = axes[1, 0]
        sleep = [v for v in data.get('sleep_hours', []) if v is not None]
        sleep_dates = [dates[i] for i, v in enumerate(data.get('sleep_hours', [])) if v is not None]
        
        if sleep:
            ax3.bar(sleep_dates[-len(sleep):], sleep, color='purple', alpha=0.7)
            ax3.set_title('Sleep Hours')
            ax3.set_ylabel('Hours')
            ax3.grid(True, alpha=0.3)
            ax3.tick_params(axis='x', rotation=45)
        
        # Mood & Stress Chart
        ax4 = axes[1, 1]
        mood = [v for v in data.get('mood_score', []) if v is not None]
        stress = [v for v in data.get('stress_level', []) if v is not None]
        mood_dates = [dates[i] for i, v in enumerate(data.get('mood_score', [])) if v is not None]
        stress_dates = [dates[i] for i, v in enumerate(data.get('stress_level', [])) if v is not None]
        
        if mood or stress:
            if mood:
                ax4.plot(mood_dates[-len(mood):], mood, 'yo-', label='Mood', linewidth=2)
            if stress:
                ax4.plot(stress_dates[-len(stress):], stress, 'ro-', label='Stress', linewidth=2)
            ax4.set_title('Mood & Stress Levels')
            ax4.set_ylabel('Score (1-10)')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
            ax4.tick_params(axis='x', rotation=45)
        
        self.figure.tight_layout()
        self.canvas.draw()

class HealthDataInputForm(QMainWindow):
    """Main health data input form application"""
    
    def __init__(self):
        super().__init__()
        self.api_base_url = "http://localhost:8000"
        self.submission_thread = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Health Tracker - Data Input Form")
        self.setGeometry(100, 100, 1000, 800)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #3498db;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Health Data Input Tab
        input_tab = self.create_input_tab()
        tab_widget.addTab(input_tab, "📊 Health Data Input")
        
        # Data Visualization Tab
        viz_tab = HealthDataVisualization()
        tab_widget.addTab(viz_tab, "📈 Data Visualization")
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        central_widget.setLayout(main_layout)
        
    def create_input_tab(self):
        """Create the health data input tab"""
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Health Data Entry Form")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 20px;")
        scroll_layout.addWidget(title_label)
        
        # Create form sections
        form_layout = QGridLayout()
        
        # Blood Pressure Section
        bp_frame = self.create_section_frame("🩺 Blood Pressure")
        bp_layout = QFormLayout()
        
        self.systolic_input = QSpinBox()
        self.systolic_input.setRange(70, 250)
        self.systolic_input.setSuffix(" mmHg")
        self.systolic_input.setToolTip("Normal range: 90-120 mmHg")
        
        self.diastolic_input = QSpinBox()
        self.diastolic_input.setRange(40, 150)
        self.diastolic_input.setSuffix(" mmHg")
        self.diastolic_input.setToolTip("Normal range: 60-80 mmHg")
        
        bp_layout.addRow("Systolic Pressure:", self.systolic_input)
        bp_layout.addRow("Diastolic Pressure:", self.diastolic_input)
        bp_frame.setLayout(bp_layout)
        
        # Blood Sugar Section
        bs_frame = self.create_section_frame("🩸 Blood Sugar")
        bs_layout = QFormLayout()
        
        self.blood_sugar_input = QDoubleSpinBox()
        self.blood_sugar_input.setRange(30, 600)
        self.blood_sugar_input.setSuffix(" mg/dL")
        self.blood_sugar_input.setDecimals(1)
        
        self.sugar_test_type = QComboBox()
        self.sugar_test_type.addItems(["", "fasting", "after_meal", "random"])
        
        bs_layout.addRow("Blood Sugar Level:", self.blood_sugar_input)
        bs_layout.addRow("Test Type:", self.sugar_test_type)
        bs_frame.setLayout(bs_layout)
        
        # Sleep Section
        sleep_frame = self.create_section_frame("😴 Sleep & Rest")
        sleep_layout = QFormLayout()
        
        self.sleep_hours_input = QDoubleSpinBox()
        self.sleep_hours_input.setRange(0, 24)
        self.sleep_hours_input.setSuffix(" hours")
        self.sleep_hours_input.setDecimals(1)
        
        self.sleep_quality_input = QSpinBox()
        self.sleep_quality_input.setRange(1, 10)
        self.sleep_quality_input.setToolTip("Rate your sleep quality (1=Poor, 10=Excellent)")
        
        sleep_layout.addRow("Sleep Duration:", self.sleep_hours_input)
        sleep_layout.addRow("Sleep Quality (1-10):", self.sleep_quality_input)
        sleep_frame.setLayout(sleep_layout)
        
        # Physical Activity Section
        activity_frame = self.create_section_frame("🏃 Physical Activity")
        activity_layout = QFormLayout()
        
        self.steps_input = QSpinBox()
        self.steps_input.setRange(0, 100000)
        self.steps_input.setSuffix(" steps")
        
        self.exercise_minutes_input = QDoubleSpinBox()
        self.exercise_minutes_input.setRange(0, 1440)
        self.exercise_minutes_input.setSuffix(" minutes")
        self.exercise_minutes_input.setDecimals(0)
        
        activity_layout.addRow("Steps Count:", self.steps_input)
        activity_layout.addRow("Exercise Duration:", self.exercise_minutes_input)
        activity_frame.setLayout(activity_layout)
        
        # Physical Measurements Section
        measurements_frame = self.create_section_frame("📏 Physical Measurements")
        measurements_layout = QFormLayout()
        
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(20, 500)
        self.weight_input.setSuffix(" kg")
        self.weight_input.setDecimals(1)
        
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(50, 300)
        self.height_input.setSuffix(" cm")
        self.height_input.setDecimals(0)
        
        self.heart_rate_input = QSpinBox()
        self.heart_rate_input.setRange(30, 250)
        self.heart_rate_input.setSuffix(" bpm")
        
        measurements_layout.addRow("Weight:", self.weight_input)
        measurements_layout.addRow("Height:", self.height_input)
        measurements_layout.addRow("Heart Rate:", self.heart_rate_input)
        measurements_frame.setLayout(measurements_layout)
        
        # Lifestyle Section
        lifestyle_frame = self.create_section_frame("🌱 Lifestyle & Wellness")
        lifestyle_layout = QFormLayout()
        
        self.water_intake_input = QDoubleSpinBox()
        self.water_intake_input.setRange(0, 20)
        self.water_intake_input.setSuffix(" liters")
        self.water_intake_input.setDecimals(1)
        
        self.mood_score_input = QSpinBox()
        self.mood_score_input.setRange(1, 10)
        self.mood_score_input.setToolTip("Rate your mood (1=Very Low, 10=Excellent)")
        
        self.energy_level_input = QSpinBox()
        self.energy_level_input.setRange(1, 10)
        self.energy_level_input.setToolTip("Rate your energy level (1=Very Low, 10=Very High)")
        
        self.stress_level_input = QSpinBox()
        self.stress_level_input.setRange(1, 10)
        self.stress_level_input.setToolTip("Rate your stress level (1=Very Low, 10=Very High)")
        
        lifestyle_layout.addRow("Water Intake:", self.water_intake_input)
        lifestyle_layout.addRow("Mood Score (1-10):", self.mood_score_input)
        lifestyle_layout.addRow("Energy Level (1-10):", self.energy_level_input)
        lifestyle_layout.addRow("Stress Level (1-10):", self.stress_level_input)
        lifestyle_frame.setLayout(lifestyle_layout)
        
        # Notes Section
        notes_frame = self.create_section_frame("📝 Additional Notes")
        notes_layout = QFormLayout()
        
        self.stress_notes_input = QLineEdit()
        self.stress_notes_input.setPlaceholderText("Describe what's causing stress...")
        
        self.general_notes_input = QTextEdit()
        self.general_notes_input.setMaximumHeight(100)
        self.general_notes_input.setPlaceholderText("Any additional health notes, symptoms, or observations...")
        
        self.measurement_time_input = QDateTimeEdit()
        self.measurement_time_input.setDateTime(QDateTime.currentDateTime())
        self.measurement_time_input.setDisplayFormat("yyyy-MM-dd hh:mm")
        
        notes_layout.addRow("Stress Notes:", self.stress_notes_input)
        notes_layout.addRow("General Notes:", self.general_notes_input)
        notes_layout.addRow("Measurement Time:", self.measurement_time_input)
        notes_frame.setLayout(notes_layout)
        
        # Add all sections to form layout
        form_layout.addWidget(bp_frame, 0, 0)
        form_layout.addWidget(bs_frame, 0, 1)
        form_layout.addWidget(sleep_frame, 1, 0)
        form_layout.addWidget(activity_frame, 1, 1)
        form_layout.addWidget(measurements_frame, 2, 0)
        form_layout.addWidget(lifestyle_frame, 2, 1)
        form_layout.addWidget(notes_frame, 3, 0, 1, 2)
        
        scroll_layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Clear Form")
        clear_btn.clicked.connect(self.clear_form)
        clear_btn.setStyleSheet("background-color: #e74c3c;")
        
        self.submit_btn = QPushButton("Submit Health Data")
        self.submit_btn.clicked.connect(self.submit_health_data)
        
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_btn)
        
        scroll_layout.addLayout(button_layout)
        
        # Progress bar for submission
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        scroll_layout.addWidget(self.progress_bar)
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        return scroll_area
        
    def create_section_frame(self, title):
        """Create a styled frame for form sections"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box)
        frame.setStyleSheet("""
            QFrame {
                border: 2px solid #3498db;
                border-radius: 8px;
                background-color: #ffffff;
                margin: 5px;
                padding: 10px;
            }
        """)
        
        # Add title label
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none; margin-bottom: 10px;")
        
        return frame
        
    def clear_form(self):
        """Clear all form inputs"""
        reply = QMessageBox.question(
            self, 
            "Clear Form", 
            "Are you sure you want to clear all data?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Reset all inputs to default values
            self.systolic_input.setValue(0)
            self.diastolic_input.setValue(0)
            self.blood_sugar_input.setValue(0)
            self.sugar_test_type.setCurrentIndex(0)
            self.sleep_hours_input.setValue(0)
            self.sleep_quality_input.setValue(1)
            self.steps_input.setValue(0)
            self.exercise_minutes_input.setValue(0)
            self.weight_input.setValue(0)
            self.height_input.setValue(0)
            self.heart_rate_input.setValue(0)
            self.water_intake_input.setValue(0)
            self.mood_score_input.setValue(1)
            self.energy_level_input.setValue(1)
            self.stress_level_input.setValue(1)
            self.stress_notes_input.clear()
            self.general_notes_input.clear()
            self.measurement_time_input.setDateTime(QDateTime.currentDateTime())
            
    def collect_form_data(self):
        """Collect data from all form inputs"""
        data = {}
        
        # Only include non-zero/non-empty values
        if self.systolic_input.value() > 0:
            data["systolic_bp"] = float(self.systolic_input.value())
        if self.diastolic_input.value() > 0:
            data["diastolic_bp"] = float(self.diastolic_input.value())
        if self.blood_sugar_input.value() > 0:
            data["blood_sugar"] = float(self.blood_sugar_input.value())
        if self.sugar_test_type.currentText():
            data["sugar_test_type"] = self.sugar_test_type.currentText()
        if self.sleep_hours_input.value() > 0:
            data["sleep_hours"] = float(self.sleep_hours_input.value())
        if self.sleep_quality_input.value() > 1:
            data["sleep_quality"] = self.sleep_quality_input.value()
        if self.steps_input.value() > 0:
            data["steps_count"] = self.steps_input.value()
        if self.exercise_minutes_input.value() > 0:
            data["exercise_minutes"] = float(self.exercise_minutes_input.value())
        if self.weight_input.value() > 0:
            data["weight"] = float(self.weight_input.value())
        if self.height_input.value() > 0:
            data["height"] = float(self.height_input.value())
        if self.heart_rate_input.value() > 0:
            data["heart_rate"] = self.heart_rate_input.value()
        if self.water_intake_input.value() > 0:
            data["water_intake"] = float(self.water_intake_input.value())
        if self.mood_score_input.value() > 1:
            data["mood_score"] = self.mood_score_input.value()
        if self.energy_level_input.value() > 1:
            data["energy_level"] = self.energy_level_input.value()
        if self.stress_level_input.value() > 1:
            data["stress_level"] = self.stress_level_input.value()
        if self.stress_notes_input.text().strip():
            data["stress_notes"] = self.stress_notes_input.text().strip()
        if self.general_notes_input.toPlainText().strip():
            data["notes"] = self.general_notes_input.toPlainText().strip()
        
        # Measurement time
        data["measurement_time"] = self.measurement_time_input.dateTime().toString(Qt.ISODate)
        
        return data
        
    def submit_health_data(self):
        """Submit health data to the API"""
        data = self.collect_form_data()
        
        if not data or len([k for k in data.keys() if k != "measurement_time"]) == 0:
            QMessageBox.warning(self, "Warning", "Please enter at least one health measurement!")
            return
        
        # Disable submit button and show progress
        self.submit_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Create and start submission thread
        api_url = f"{self.api_base_url}/api/v1/healthdata"
        self.submission_thread = HealthDataSubmissionThread(data, api_url)
        self.submission_thread.success.connect(self.on_submission_success)
        self.submission_thread.error.connect(self.on_submission_error)
        self.submission_thread.start()
        
    def on_submission_success(self, message):
        """Handle successful data submission"""
        self.submit_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        QMessageBox.information(self, "Success", message)
        
        # Ask if user wants to clear the form
        reply = QMessageBox.question(
            self,
            "Clear Form",
            "Data submitted successfully! Would you like to clear the form for new entry?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            self.clear_form()
    
    def on_submission_error(self, error_message):
        """Handle submission error"""
        self.submit_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        QMessageBox.critical(self, "Submission Error", error_message)

def main():
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Health Tracker")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Health Tracker Inc.")
    
    # Create and show main window
    window = HealthDataInputForm()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()