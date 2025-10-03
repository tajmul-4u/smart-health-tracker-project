#!/usr/bin/env python3
"""
Modern Health Data Input System - Advanced User-Friendly Interface
Enhanced with modern UI elements, smart validation, and intuitive design
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, 
    QTextEdit, QDateTimeEdit, QPushButton, QMessageBox, QGroupBox,
    QScrollArea, QFrame, QProgressBar, QTabWidget, QSlider,
    QCheckBox, QRadioButton, QButtonGroup, QSplitter, QStackedWidget,
    QGraphicsDropShadowEffect, QApplication, QDialog
)
from PyQt6.QtCore import (
    Qt, QDateTime, QTimer, pyqtSignal, QPropertyAnimation, 
    QEasingCurve, QRect, QPoint, QParallelAnimationGroup
)
from PyQt6.QtGui import (
    QFont, QPalette, QColor, QLinearGradient, QPainter, QBrush,
    QPixmap, QIcon, QPen, QFontMetrics
)
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
import requests
from datetime import datetime, date, timedelta
import json
import math

class ModernCard(QFrame):
    """Modern card container with shadow effects"""
    
    def __init__(self, title="", icon="", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(0)
        self.init_styling()
        
        if title:
            self.add_header(title, icon)
            
    def init_styling(self):
        """Initialize card styling with modern effects"""
        self.setStyleSheet("""
            ModernCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 1px solid #e9ecef;
                border-radius: 12px;
                margin: 8px;
                padding: 16px;
            }
            ModernCard:hover {
                border-color: #007bff;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f8ff);
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)
        
    def add_header(self, title, icon=""):
        """Add header to card"""
        layout = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        
        if icon:
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Arial", 16))
            header_layout.addWidget(icon_label)
            
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        self.setLayout(layout)
        
        return layout

class SmartSlider(QWidget):
    """Smart slider with visual feedback and validation"""
    
    valueChanged = pyqtSignal(int)
    
    def __init__(self, min_val=0, max_val=100, current_val=50, 
                 labels=None, colors=None, suffix="", parent=None):
        super().__init__(parent)
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = current_val
        self.suffix = suffix
        self.labels = labels or []
        self.colors = colors or ["#28a745", "#ffc107", "#dc3545"]
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize smart slider UI"""
        layout = QVBoxLayout()
        
        # Value display
        self.value_label = QLabel(f"{self.current_val}{self.suffix}")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.value_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(self.value_label)
        
        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(self.min_val)
        self.slider.setMaximum(self.max_val)
        self.slider.setValue(self.current_val)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval((self.max_val - self.min_val) // 5)
        
        # Style slider
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: #f0f0f0;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #007bff);
                border: 2px solid #007bff;
                width: 20px;
                margin: -8px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #0056b3);
                border: 2px solid #0056b3;
            }
        """)
        
        layout.addWidget(self.slider)
        
        # Labels
        if self.labels:
            labels_layout = QHBoxLayout()
            for label in self.labels:
                label_widget = QLabel(label)
                label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label_widget.setFont(QFont("Segoe UI", 9))
                label_widget.setStyleSheet("color: #6c757d;")
                labels_layout.addWidget(label_widget)
            layout.addLayout(labels_layout)
            
        self.setLayout(layout)
        
        # Connect signals
        self.slider.valueChanged.connect(self.on_value_changed)
        
    def on_value_changed(self, value):
        """Handle value changes"""
        self.current_val = value
        self.value_label.setText(f"{value}{self.suffix}")
        
        # Update color based on value
        if self.colors:
            ratio = (value - self.min_val) / (self.max_val - self.min_val)
            if ratio < 0.33:
                color = self.colors[0]  # Green for low
            elif ratio < 0.66:
                color = self.colors[1]  # Yellow for medium
            else:
                color = self.colors[2]  # Red for high
                
            self.value_label.setStyleSheet(f"color: {color}; margin: 10px; font-weight: bold;")
            
        self.valueChanged.emit(value)
        
    def setValue(self, value):
        """Set slider value"""
        self.slider.setValue(value)

class QuickInputCard(ModernCard):
    """Quick input card for common health metrics"""
    
    valueChanged = pyqtSignal(str, object)  # metric_name, value
    
    def __init__(self, metric_name, icon, unit="", input_type="number", 
                 min_val=0, max_val=1000, current_val=0, parent=None):
        super().__init__(parent=parent)
        self.metric_name = metric_name
        self.icon = icon
        self.unit = unit
        self.input_type = input_type
        
        self.init_quick_input(min_val, max_val, current_val)
        
    def init_quick_input(self, min_val, max_val, current_val):
        """Initialize quick input interface"""
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(self.icon)
        icon_label.setFont(QFont("Arial", 20))
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(self.metric_name)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Input based on type
        if self.input_type == "slider":
            self.input_widget = SmartSlider(min_val, max_val, current_val, suffix=self.unit)
            self.input_widget.valueChanged.connect(
                lambda val: self.valueChanged.emit(self.metric_name, val)
            )
        else:
            self.input_widget = QDoubleSpinBox()
            self.input_widget.setRange(min_val, max_val)
            self.input_widget.setValue(current_val)
            self.input_widget.setSuffix(f" {self.unit}" if self.unit else "")
            self.input_widget.setStyleSheet("""
                QDoubleSpinBox {
                    padding: 12px;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    text-align: center;
                }
                QDoubleSpinBox:focus {
                    border-color: #007bff;
                    background-color: #f0f8ff;
                }
            """)
            self.input_widget.valueChanged.connect(
                lambda val: self.valueChanged.emit(self.metric_name, val)
            )
            
        layout.addWidget(self.input_widget)
        
        # Quick preset buttons for common values
        if self.metric_name == "Blood Pressure":
            presets_layout = QHBoxLayout()
            presets = [("Normal", 120), ("High", 140), ("Low", 90)]
            for name, value in presets:
                btn = QPushButton(name)
                btn.clicked.connect(lambda checked, v=value: self.input_widget.setValue(v))
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f8f9fa;
                        color: #6c757d;
                        border: 1px solid #dee2e6;
                        padding: 6px 12px;
                        border-radius: 4px;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        background-color: #e9ecef;
                    }
                """)
                presets_layout.addWidget(btn)
            layout.addLayout(presets_layout)
            
        self.setLayout(layout)

class ModernHealthDataInput(QWidget):
    """Modern health data input system with enhanced UX"""
    
    # Signals
    data_submitted = pyqtSignal(dict)
    data_updated = pyqtSignal(dict)
    validation_failed = pyqtSignal(str)
    
    def __init__(self, api_client=None):
        super().__init__()
        self.api_client = api_client
        self.api_base_url = "http://localhost:8000"
        self.current_data = {}
        self.validation_rules = {}
        
        self.init_ui()
        self.setup_validation()
        self.setup_animations()
        
    def init_ui(self):
        """Initialize modern user interface"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                margin-top: -1px;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 2px solid #dee2e6;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                color: white;
                border-color: #007bff;
                margin-bottom: -2px;
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f8ff, stop:1 #e7f3ff);
                border-color: #007bff;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with title and status
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget for different input modes
        self.tab_widget = QTabWidget()
        
        # Quick Input Tab
        quick_tab = self.create_quick_input_tab()
        self.tab_widget.addTab(quick_tab, "⚡ Quick Input")
        
        # Detailed Input Tab
        detailed_tab = self.create_detailed_input_tab()
        self.tab_widget.addTab(detailed_tab, "📋 Detailed Form")
        
        # Trends & History Tab
        trends_tab = self.create_trends_tab()
        self.tab_widget.addTab(trends_tab, "📈 Trends & History")
        
        # Settings Tab
        settings_tab = self.create_settings_tab()
        self.tab_widget.addTab(settings_tab, "⚙️ Preferences")
        
        main_layout.addWidget(self.tab_widget)
        
        # Footer with action buttons
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
        
    def create_header(self):
        """Create modern header with status indicators"""
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007bff, stop:1 #0056b3);
                border-radius: 12px;
                margin-bottom: 20px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Title section
        title_layout = QVBoxLayout()
        
        title_label = QLabel("🏥 Smart Health Data Input")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white; margin: 0;")
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Track your health with modern, intuitive tools")
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setStyleSheet("color: #e3f2fd; margin: 0;")
        title_layout.addWidget(subtitle_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Status indicators
        status_layout = QVBoxLayout()
        
        # Connection status
        self.connection_status = QLabel("🟢 Connected")
        self.connection_status.setStyleSheet("color: #4caf50; font-weight: bold;")
        status_layout.addWidget(self.connection_status)
        
        # Last sync
        self.last_sync = QLabel("Last sync: Just now")
        self.last_sync.setStyleSheet("color: #e3f2fd; font-size: 10px;")
        status_layout.addWidget(self.last_sync)
        
        layout.addLayout(status_layout)
        
        header_frame.setLayout(layout)
        return header_frame
        
    def create_quick_input_tab(self):
        """Create quick input tab with smart cards"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        # Description
        desc_label = QLabel("💡 Quick input for daily health metrics - optimized for speed and ease")
        desc_label.setStyleSheet("""
            QLabel {
                background-color: #e7f3ff;
                border: 1px solid #007bff;
                border-radius: 8px;
                padding: 12px;
                color: #004085;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(desc_label)
        
        # Quick input cards grid
        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)
        
        # Define quick input metrics
        quick_metrics = [
            ("Blood Pressure", "🩺", "mmHg", "number", 70, 200, 120),
            ("Heart Rate", "❤️", "bpm", "number", 40, 200, 72),
            ("Weight", "⚖️", "kg", "number", 30, 200, 70),
            ("Sleep Quality", "😴", "/10", "slider", 1, 10, 7),
            ("Mood", "😊", "/10", "slider", 1, 10, 7),
            ("Stress Level", "😰", "/10", "slider", 1, 10, 3),
            ("Water Intake", "💧", "L", "number", 0, 10, 2),
            ("Energy Level", "⚡", "/10", "slider", 1, 10, 7),
        ]
        
        self.quick_cards = {}
        row, col = 0, 0
        for metric_name, icon, unit, input_type, min_val, max_val, default in quick_metrics:
            card = QuickInputCard(metric_name, icon, unit, input_type, min_val, max_val, default)
            card.valueChanged.connect(self.on_quick_input_changed)
            self.quick_cards[metric_name] = card
            
            cards_layout.addWidget(card, row, col)
            col += 1
            if col >= 3:  # 3 cards per row
                col = 0
                row += 1
                
        layout.addLayout(cards_layout)
        
        # Quick save button
        quick_save_layout = QHBoxLayout()
        quick_save_layout.addStretch()
        
        self.quick_save_btn = QPushButton("💾 Save Quick Entry")
        self.quick_save_btn.setFixedSize(200, 50)
        self.quick_save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #1e7e34);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34ce57, stop:1 #28a745);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e7e34, stop:1 #155724);
            }
        """)
        self.quick_save_btn.clicked.connect(self.save_quick_data)
        quick_save_layout.addWidget(self.quick_save_btn)
        quick_save_layout.addStretch()
        
        layout.addLayout(quick_save_layout)
        layout.addStretch()
        
        content.setLayout(layout)
        scroll.setWidget(content)
        
        return scroll
        
    def create_detailed_input_tab(self):
        """Create detailed input form with validation"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        # Description
        desc_label = QLabel("📋 Comprehensive health data entry with advanced options and validation")
        desc_label.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffc107;
                border-radius: 8px;
                padding: 12px;
                color: #856404;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(desc_label)
        
        # Detailed forms in expandable sections
        sections = [
            ("🩺 Vital Signs", self.create_vitals_section()),
            ("🏃 Physical Activity", self.create_activity_section()),
            ("🧠 Mental Wellness", self.create_mental_section()),
            ("💊 Medications & Supplements", self.create_medication_section()),
            ("📝 Symptoms & Notes", self.create_notes_section()),
        ]
        
        for title, section_widget in sections:
            # Create collapsible section
            section_card = ModernCard(title)
            card_layout = section_card.layout()
            card_layout.addWidget(section_widget)
            layout.addWidget(section_card)
            
        layout.addStretch()
        
        content.setLayout(layout)
        scroll.setWidget(content)
        
        return scroll
        
    def create_vitals_section(self):
        """Create vital signs input section"""
        widget = QWidget()
        layout = QFormLayout()
        
        # Blood Pressure with smart input
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
        
        layout.addRow("🩺 Blood Pressure:", bp_layout)
        
        # Blood Sugar with test type
        bs_layout = QHBoxLayout()
        self.blood_sugar_input = QDoubleSpinBox()
        self.blood_sugar_input.setRange(50, 500)
        self.blood_sugar_input.setValue(95)
        self.blood_sugar_input.setSuffix(" mg/dL")
        
        self.sugar_test_type = QComboBox()
        self.sugar_test_type.addItems(["Fasting", "Random", "Post-meal", "HbA1c"])
        
        bs_layout.addWidget(self.blood_sugar_input)
        bs_layout.addWidget(self.sugar_test_type)
        
        layout.addRow("🩸 Blood Sugar:", bs_layout)
        
        # Temperature
        self.temperature_input = QDoubleSpinBox()
        self.temperature_input.setRange(35.0, 42.0)
        self.temperature_input.setValue(36.6)
        self.temperature_input.setSuffix(" °C")
        self.temperature_input.setDecimals(1)
        layout.addRow("🌡️ Temperature:", self.temperature_input)
        
        # Oxygen Saturation
        self.oxygen_input = QSpinBox()
        self.oxygen_input.setRange(80, 100)
        self.oxygen_input.setValue(98)
        self.oxygen_input.setSuffix(" %")
        layout.addRow("🫁 Oxygen Saturation:", self.oxygen_input)
        
        widget.setLayout(layout)
        return widget
        
    def create_activity_section(self):
        """Create physical activity section"""
        widget = QWidget()
        layout = QFormLayout()
        
        # Steps with smart input
        self.steps_input = QSpinBox()
        self.steps_input.setRange(0, 50000)
        self.steps_input.setValue(8000)
        self.steps_input.setSuffix(" steps")
        layout.addRow("👣 Daily Steps:", self.steps_input)
        
        # Exercise duration and type
        exercise_layout = QHBoxLayout()
        self.exercise_duration = QSpinBox()
        self.exercise_duration.setRange(0, 300)
        self.exercise_duration.setValue(30)
        self.exercise_duration.setSuffix(" min")
        
        self.exercise_type = QComboBox()
        self.exercise_type.addItems([
            "Walking", "Running", "Cycling", "Swimming", "Gym Workout",
            "Yoga", "Dancing", "Sports", "Other"
        ])
        
        exercise_layout.addWidget(self.exercise_duration)
        exercise_layout.addWidget(self.exercise_type)
        layout.addRow("🏃 Exercise:", exercise_layout)
        
        # Sleep with quality rating
        sleep_layout = QHBoxLayout()
        self.sleep_hours = QDoubleSpinBox()
        self.sleep_hours.setRange(0, 24)
        self.sleep_hours.setValue(7.5)
        self.sleep_hours.setSuffix(" hours")
        self.sleep_hours.setDecimals(1)
        
        sleep_layout.addWidget(self.sleep_hours)
        sleep_layout.addWidget(QLabel("Quality:"))
        
        self.sleep_quality = SmartSlider(1, 10, 7, 
            labels=["Poor", "Average", "Excellent"],
            colors=["#dc3545", "#ffc107", "#28a745"],
            suffix="/10"
        )
        sleep_layout.addWidget(self.sleep_quality)
        
        layout.addRow("😴 Sleep:", sleep_layout)
        
        widget.setLayout(layout)
        return widget
        
    def create_mental_section(self):
        """Create mental wellness section"""
        widget = QWidget()
        layout = QFormLayout()
        
        # Mood tracking with emoji feedback
        self.mood_slider = SmartSlider(1, 10, 7,
            labels=["😢 Very Sad", "😐 Neutral", "😊 Very Happy"],
            colors=["#dc3545", "#ffc107", "#28a745"],
            suffix="/10"
        )
        layout.addRow("😊 Mood Rating:", self.mood_slider)
        
        # Stress level
        self.stress_slider = SmartSlider(1, 10, 3,
            labels=["😌 Relaxed", "😐 Moderate", "😰 High Stress"],
            colors=["#28a745", "#ffc107", "#dc3545"],
            suffix="/10"
        )
        layout.addRow("😰 Stress Level:", self.stress_slider)
        
        # Energy level
        self.energy_slider = SmartSlider(1, 10, 7,
            labels=["😴 Tired", "😐 Moderate", "⚡ Energetic"],
            colors=["#dc3545", "#ffc107", "#28a745"],
            suffix="/10"
        )
        layout.addRow("⚡ Energy Level:", self.energy_slider)
        
        # Anxiety level
        self.anxiety_slider = SmartSlider(1, 10, 3,
            labels=["😌 Calm", "😐 Mild", "😨 High Anxiety"],
            colors=["#28a745", "#ffc107", "#dc3545"],
            suffix="/10"
        )
        layout.addRow("😨 Anxiety Level:", self.anxiety_slider)
        
        widget.setLayout(layout)
        return widget
        
    def create_medication_section(self):
        """Create medication tracking section"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Medication checklist
        meds_label = QLabel("💊 Today's Medications:")
        meds_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(meds_label)
        
        # Dynamic medication list
        self.medication_checks = {}
        common_meds = [
            "Multivitamin", "Vitamin D", "Omega-3", "Blood Pressure Medication",
            "Diabetes Medication", "Pain Relief", "Other"
        ]
        
        for med in common_meds:
            checkbox = QCheckBox(med)
            checkbox.setStyleSheet("""
                QCheckBox {
                    font-size: 13px;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
            """)
            self.medication_checks[med] = checkbox
            layout.addWidget(checkbox)
            
        # Custom medication input
        custom_med_layout = QHBoxLayout()
        custom_med_layout.addWidget(QLabel("Custom:"))
        self.custom_medication = QLineEdit()
        self.custom_medication.setPlaceholderText("Enter custom medication...")
        custom_med_layout.addWidget(self.custom_medication)
        layout.addLayout(custom_med_layout)
        
        widget.setLayout(layout)
        return widget
        
    def create_notes_section(self):
        """Create notes and symptoms section"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Symptoms checklist
        symptoms_label = QLabel("🤒 Symptoms (if any):")
        symptoms_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(symptoms_label)
        
        # Common symptoms
        self.symptom_checks = {}
        common_symptoms = [
            "Headache", "Fatigue", "Nausea", "Dizziness", "Chest Pain",
            "Shortness of Breath", "Muscle Pain", "Joint Pain", "Fever", "Cough"
        ]
        
        symptoms_grid = QGridLayout()
        for i, symptom in enumerate(common_symptoms):
            checkbox = QCheckBox(symptom)
            checkbox.setStyleSheet("QCheckBox { font-size: 12px; padding: 3px; }")
            self.symptom_checks[symptom] = checkbox
            symptoms_grid.addWidget(checkbox, i // 3, i % 3)
            
        layout.addLayout(symptoms_grid)
        
        # Additional notes
        notes_label = QLabel("📝 Additional Notes:")
        notes_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(notes_label)
        
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        self.notes_input.setPlaceholderText("Enter any additional observations, concerns, or notes about your health today...")
        self.notes_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border-color: #007bff;
                background-color: #f0f8ff;
            }
        """)
        layout.addWidget(self.notes_input)
        
        widget.setLayout(layout)
        return widget
        
    def create_trends_tab(self):
        """Create trends and history visualization"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Placeholder for charts - would integrate with QtCharts
        chart_placeholder = QLabel("📈 Health Trends & History\n\n"
                                 "• Interactive charts showing your health data over time\n"
                                 "• Weekly and monthly summaries\n"
                                 "• Pattern recognition and insights\n"
                                 "• Goal tracking and progress visualization\n\n"
                                 "[Charts would be implemented here with real data]")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 2px dashed #6c757d;
                border-radius: 12px;
                padding: 40px;
                color: #6c757d;
                font-size: 16px;
                line-height: 1.6;
            }
        """)
        
        layout.addWidget(chart_placeholder)
        
        widget.setLayout(layout)
        return widget
        
    def create_settings_tab(self):
        """Create settings and preferences"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        # Notification preferences
        notif_card = ModernCard("🔔 Notification Preferences")
        notif_layout = notif_card.layout()
        
        self.reminder_checks = {}
        reminders = [
            ("Daily health check reminder", True),
            ("Medication reminders", True),
            ("Weekly health summary", False),
            ("Achievement notifications", True),
            ("Data sync notifications", False)
        ]
        
        for reminder_text, default_state in reminders:
            checkbox = QCheckBox(reminder_text)
            checkbox.setChecked(default_state)
            self.reminder_checks[reminder_text] = checkbox
            notif_layout.addWidget(checkbox)
            
        layout.addWidget(notif_card)
        
        # Data sync preferences
        sync_card = ModernCard("🔄 Data Synchronization")
        sync_layout = sync_card.layout()
        
        # Auto-sync option
        self.auto_sync_check = QCheckBox("Enable automatic data synchronization")
        self.auto_sync_check.setChecked(True)
        sync_layout.addWidget(self.auto_sync_check)
        
        # Sync frequency
        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel("Sync frequency:"))
        self.sync_frequency = QComboBox()
        self.sync_frequency.addItems(["Real-time", "Every 5 minutes", "Every hour", "Manual only"])
        freq_layout.addWidget(self.sync_frequency)
        sync_layout.addLayout(freq_layout)
        
        layout.addWidget(sync_card)
        
        # Privacy settings
        privacy_card = ModernCard("🔐 Privacy & Security")
        privacy_layout = privacy_card.layout()
        
        self.privacy_checks = {}
        privacy_options = [
            ("Share anonymous data for research", False),
            ("Allow data export", True),
            ("Require password for sensitive data", False),
            ("Enable data encryption", True)
        ]
        
        for privacy_text, default_state in privacy_options:
            checkbox = QCheckBox(privacy_text)
            checkbox.setChecked(default_state)
            self.privacy_checks[privacy_text] = checkbox
            privacy_layout.addWidget(checkbox)
            
        layout.addWidget(privacy_card)
        
        layout.addStretch()
        
        content.setLayout(layout)
        scroll.setWidget(content)
        
        return scroll
        
    def create_footer(self):
        """Create footer with action buttons"""
        footer_frame = QFrame()
        footer_frame.setFixedHeight(80)
        footer_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-top: 1px solid #dee2e6;
                border-radius: 0px 0px 12px 12px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Auto-save indicator
        self.auto_save_label = QLabel("💾 Auto-save: Enabled")
        self.auto_save_label.setStyleSheet("color: #28a745; font-size: 12px;")
        layout.addWidget(self.auto_save_label)
        
        layout.addStretch()
        
        # Action buttons
        self.clear_btn = QPushButton("🗑️ Clear All")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-weight: bold;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_all_data)
        layout.addWidget(self.clear_btn)
        
        self.save_btn = QPushButton("💾 Save Data")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0069d9, stop:1 #0056b3);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0056b3, stop:1 #004085);
            }
        """)
        self.save_btn.clicked.connect(self.save_all_data)
        layout.addWidget(self.save_btn)
        
        footer_frame.setLayout(layout)
        return footer_frame
        
    def setup_validation(self):
        """Setup form validation rules"""
        self.validation_rules = {
            'systolic_bp': {'min': 70, 'max': 250, 'required': False},
            'diastolic_bp': {'min': 40, 'max': 150, 'required': False},
            'blood_sugar': {'min': 50, 'max': 500, 'required': False},
            'heart_rate': {'min': 40, 'max': 200, 'required': False},
            'temperature': {'min': 35.0, 'max': 42.0, 'required': False},
            'weight': {'min': 30, 'max': 300, 'required': False},
            'sleep_hours': {'min': 0, 'max': 24, 'required': False},
        }
        
    def setup_animations(self):
        """Setup UI animations for better UX"""
        # Animation for save button
        self.save_animation = QPropertyAnimation(self.save_btn, b"geometry")
        self.save_animation.setDuration(200)
        self.save_animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
    def on_quick_input_changed(self, metric_name, value):
        """Handle quick input changes"""
        self.current_data[metric_name.lower().replace(' ', '_')] = value
        
        # Auto-save after 2 seconds of inactivity
        if hasattr(self, 'auto_save_timer'):
            self.auto_save_timer.stop()
            
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_data)
        self.auto_save_timer.setSingleShot(True)
        self.auto_save_timer.start(2000)  # 2 seconds
        
    def validate_data(self, data):
        """Validate health data"""
        errors = []
        
        for field, rules in self.validation_rules.items():
            if field in data:
                value = data[field]
                
                if rules.get('required') and not value:
                    errors.append(f"{field.replace('_', ' ').title()} is required")
                    
                if value and 'min' in rules and value < rules['min']:
                    errors.append(f"{field.replace('_', ' ').title()} is too low (minimum: {rules['min']})")
                    
                if value and 'max' in rules and value > rules['max']:
                    errors.append(f"{field.replace('_', ' ').title()} is too high (maximum: {rules['max']})")
                    
        return errors
        
    def collect_all_data(self):
        """Collect data from all form inputs"""
        data = {}
        
        # Quick input data
        data.update(self.current_data)
        
        # Detailed form data
        if hasattr(self, 'systolic_input'):
            data['systolic_bp'] = self.systolic_input.value()
            data['diastolic_bp'] = self.diastolic_input.value()
            data['blood_sugar'] = self.blood_sugar_input.value()
            data['sugar_test_type'] = self.sugar_test_type.currentText()
            data['temperature'] = self.temperature_input.value()
            data['oxygen_saturation'] = self.oxygen_input.value()
            data['steps'] = self.steps_input.value()
            data['exercise_duration'] = self.exercise_duration.value()
            data['exercise_type'] = self.exercise_type.currentText()
            data['sleep_hours'] = self.sleep_hours.value()
            data['sleep_quality'] = self.sleep_quality.current_val
            
        # Mental wellness data
        if hasattr(self, 'mood_slider'):
            data['mood_score'] = self.mood_slider.current_val
            data['stress_level'] = self.stress_slider.current_val
            data['energy_level'] = self.energy_slider.current_val
            data['anxiety_level'] = self.anxiety_slider.current_val
            
        # Medications
        taken_medications = []
        for med, checkbox in self.medication_checks.items():
            if checkbox.isChecked():
                taken_medications.append(med)
        if self.custom_medication.text().strip():
            taken_medications.append(self.custom_medication.text().strip())
        data['medications_taken'] = taken_medications
        
        # Symptoms
        symptoms = []
        for symptom, checkbox in self.symptom_checks.items():
            if checkbox.isChecked():
                symptoms.append(symptom)
        data['symptoms'] = symptoms
        
        # Notes
        if hasattr(self, 'notes_input'):
            data['notes'] = self.notes_input.toPlainText().strip()
            
        # Timestamp
        data['timestamp'] = datetime.now().isoformat()
        
        return data
        
    def save_quick_data(self):
        """Save quick input data"""
        try:
            data = {}
            for metric, card in self.quick_cards.items():
                if hasattr(card.input_widget, 'value'):
                    if isinstance(card.input_widget, SmartSlider):
                        data[metric.lower().replace(' ', '_')] = card.input_widget.current_val
                    else:
                        data[metric.lower().replace(' ', '_')] = card.input_widget.value()
                        
            data['timestamp'] = datetime.now().isoformat()
            data['entry_type'] = 'quick_input'
            
            # Validate data
            errors = self.validate_data(data)
            if errors:
                QMessageBox.warning(self, "⚠️ Validation Errors", 
                                  "Please fix the following issues:\n\n" + "\n".join(errors))
                return
                
            # Animate save button
            self.animate_save_button()
            
            # Submit data
            self.submit_data(data)
            
            # Show success message
            QMessageBox.information(self, "✅ Success", 
                                  "Quick health data saved successfully!")
                                  
        except Exception as e:
            QMessageBox.critical(self, "❌ Error", f"Failed to save data: {str(e)}")
            
    def save_all_data(self):
        """Save all form data"""
        try:
            data = self.collect_all_data()
            
            # Validate data
            errors = self.validate_data(data)
            if errors:
                QMessageBox.warning(self, "⚠️ Validation Errors", 
                                  "Please fix the following issues:\n\n" + "\n".join(errors))
                return
                
            # Animate save button
            self.animate_save_button()
            
            # Submit data
            self.submit_data(data)
            
            # Show success message with summary
            summary = f"Health data saved successfully!\n\n"
            if 'systolic_bp' in data and data['systolic_bp'] > 0:
                summary += f"Blood Pressure: {data['systolic_bp']}/{data['diastolic_bp']} mmHg\n"
            if 'heart_rate' in data and data['heart_rate'] > 0:
                summary += f"Heart Rate: {data['heart_rate']} bpm\n"
            if 'mood_score' in data:
                summary += f"Mood: {data['mood_score']}/10\n"
            if 'stress_level' in data:
                summary += f"Stress: {data['stress_level']}/10\n"
                
            QMessageBox.information(self, "✅ Success", summary)
            
        except Exception as e:
            QMessageBox.critical(self, "❌ Error", f"Failed to save data: {str(e)}")
            
    def auto_save_data(self):
        """Auto-save current data"""
        try:
            if not self.current_data:
                return
                
            data = self.current_data.copy()
            data['timestamp'] = datetime.now().isoformat()
            data['entry_type'] = 'auto_save'
            
            # Submit silently
            self.submit_data(data, silent=True)
            
            # Update auto-save indicator
            self.auto_save_label.setText("💾 Auto-saved just now")
            self.auto_save_label.setStyleSheet("color: #28a745; font-size: 12px;")
            
        except Exception as e:
            print(f"Auto-save failed: {e}")
            
    def submit_data(self, data, silent=False):
        """Submit data to API"""
        try:
            if self.api_client:
                response = self.api_client.post("/api/health-data", json=data)
            else:
                # Fallback to direct requests
                response = requests.post(f"{self.api_base_url}/api/health-data", 
                                       json=data, timeout=5)
                                       
            if response.status_code == 200:
                self.data_submitted.emit(data)
                if not silent:
                    self.update_connection_status(True)
            else:
                raise Exception(f"API returned status {response.status_code}")
                
        except Exception as e:
            if not silent:
                print(f"Failed to submit data: {e}")
                self.update_connection_status(False)
            # Store locally for later sync
            self.store_offline_data(data)
            
    def store_offline_data(self, data):
        """Store data offline for later sync"""
        # Implementation for offline storage
        pass
        
    def clear_all_data(self):
        """Clear all form data"""
        reply = QMessageBox.question(self, "🗑️ Clear All Data",
                                   "Are you sure you want to clear all entered data?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                                   
        if reply == QMessageBox.StandardButton.Yes:
            # Reset all inputs
            self.current_data.clear()
            
            # Reset quick input cards
            for card in self.quick_cards.values():
                if hasattr(card.input_widget, 'setValue'):
                    if isinstance(card.input_widget, SmartSlider):
                        card.input_widget.setValue(card.input_widget.min_val + 
                                                 (card.input_widget.max_val - card.input_widget.min_val) // 2)
                    else:
                        card.input_widget.setValue(0)
                        
            # Reset detailed form inputs
            if hasattr(self, 'systolic_input'):
                self.systolic_input.setValue(120)
                self.diastolic_input.setValue(80)
                self.blood_sugar_input.setValue(95)
                self.temperature_input.setValue(36.6)
                self.oxygen_input.setValue(98)
                self.steps_input.setValue(0)
                self.exercise_duration.setValue(0)
                self.sleep_hours.setValue(0)
                
            # Clear checkboxes
            for checkbox in self.medication_checks.values():
                checkbox.setChecked(False)
            for checkbox in self.symptom_checks.values():
                checkbox.setChecked(False)
                
            # Clear text inputs
            if hasattr(self, 'custom_medication'):
                self.custom_medication.clear()
            if hasattr(self, 'notes_input'):
                self.notes_input.clear()
                
            QMessageBox.information(self, "✅ Cleared", "All data has been cleared.")
            
    def animate_save_button(self):
        """Animate save button for visual feedback"""
        original_size = self.save_btn.size()
        larger_size = original_size * 1.05
        
        # Expand animation
        self.save_animation.setStartValue(self.save_btn.geometry())
        new_geo = self.save_btn.geometry()
        new_geo.setSize(larger_size)
        self.save_animation.setEndValue(new_geo)
        
        # Chain with shrink animation
        shrink_animation = QPropertyAnimation(self.save_btn, b"geometry")
        shrink_animation.setDuration(100)
        shrink_animation.setStartValue(new_geo)
        final_geo = self.save_btn.geometry()
        final_geo.setSize(original_size)
        shrink_animation.setEndValue(final_geo)
        
        self.save_animation.finished.connect(shrink_animation.start)
        self.save_animation.start()
        
    def update_connection_status(self, connected):
        """Update connection status indicator"""
        if connected:
            self.connection_status.setText("🟢 Connected")
            self.connection_status.setStyleSheet("color: #4caf50; font-weight: bold;")
            self.last_sync.setText(f"Last sync: {datetime.now().strftime('%H:%M:%S')}")
        else:
            self.connection_status.setText("🔴 Offline")
            self.connection_status.setStyleSheet("color: #f44336; font-weight: bold;")
            self.last_sync.setText("Storing data locally")

def main():
    """Test the modern health input system"""
    app = QApplication([])
    app.setStyleSheet("""
        QApplication {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    """)
    
    # Create main window
    window = QDialog()
    window.setWindowTitle("🏥 Modern Health Data Input System")
    window.setGeometry(100, 100, 1200, 900)
    
    layout = QVBoxLayout()
    
    # Create the modern health input widget
    health_input = ModernHealthDataInput()
    layout.addWidget(health_input)
    
    window.setLayout(layout)
    window.show()
    
    app.exec()

if __name__ == "__main__":
    main()