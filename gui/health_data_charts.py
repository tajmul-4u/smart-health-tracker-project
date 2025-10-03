"""
Health Data Visualization Component using PyQtGraph for better performance
"""
import sys
import requests
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QComboBox, QLabel, QMessageBox, QTabWidget, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
import numpy as np

class HealthDataCharts(QWidget):
    """Health data visualization using PyQtGraph charts"""
    
    def __init__(self, api_base_url="http://localhost:8000"):
        super().__init__()
        self.api_base_url = api_base_url
        self.chart_data = {}
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Control panel
        control_panel = QHBoxLayout()
        
        # Time period selector
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Last 7 days", "Last 30 days", "Last 90 days", "Last 180 days"])
        self.period_combo.currentTextChanged.connect(self.on_period_changed)
        
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.clicked.connect(self.load_data)
        
        control_panel.addWidget(QLabel("Time Period:"))
        control_panel.addWidget(self.period_combo)
        control_panel.addStretch()
        control_panel.addWidget(refresh_btn)
        
        layout.addLayout(control_panel)
        
        # Create tab widget for different chart categories
        self.tab_widget = QTabWidget()
        
        # Vital Signs Tab
        vital_signs_tab = self.create_vital_signs_tab()
        self.tab_widget.addTab(vital_signs_tab, "Vital Signs")
        
        # Lifestyle Tab
        lifestyle_tab = self.create_lifestyle_tab()
        self.tab_widget.addTab(lifestyle_tab, "Lifestyle")
        
        # Physical Activity Tab
        activity_tab = self.create_activity_tab()
        self.tab_widget.addTab(activity_tab, "Physical Activity")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
        # Set up auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_data)
        self.refresh_timer.start(300000)  # Refresh every 5 minutes
        
    def create_vital_signs_tab(self):
        """Create vital signs charts tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Blood Pressure Chart
        self.bp_plot = pg.PlotWidget(title="Blood Pressure Trends")
        self.bp_plot.setLabel('left', 'Pressure', units='mmHg')
        self.bp_plot.setLabel('bottom', 'Date')
        self.bp_plot.addLegend()
        self.bp_plot.showGrid(x=True, y=True)
        layout.addWidget(self.bp_plot)
        
        # Blood Sugar Chart
        self.bs_plot = pg.PlotWidget(title="Blood Sugar Levels")
        self.bs_plot.setLabel('left', 'Blood Sugar', units='mg/dL')
        self.bs_plot.setLabel('bottom', 'Date')
        self.bs_plot.showGrid(x=True, y=True)
        layout.addWidget(self.bs_plot)
        
        # Heart Rate Chart
        self.hr_plot = pg.PlotWidget(title="Heart Rate")
        self.hr_plot.setLabel('left', 'Heart Rate', units='bpm')
        self.hr_plot.setLabel('bottom', 'Date')
        self.hr_plot.showGrid(x=True, y=True)
        layout.addWidget(self.hr_plot)
        
        widget.setLayout(layout)
        return widget
        
    def create_lifestyle_tab(self):
        """Create lifestyle charts tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Sleep Chart
        self.sleep_plot = pg.PlotWidget(title="Sleep Patterns")
        self.sleep_plot.setLabel('left', 'Hours')
        self.sleep_plot.setLabel('bottom', 'Date')
        self.sleep_plot.showGrid(x=True, y=True)
        layout.addWidget(self.sleep_plot)
        
        # Mood & Stress Chart
        self.mood_stress_plot = pg.PlotWidget(title="Mood & Stress Levels")
        self.mood_stress_plot.setLabel('left', 'Score (1-10)')
        self.mood_stress_plot.setLabel('bottom', 'Date')
        self.mood_stress_plot.addLegend()
        self.mood_stress_plot.showGrid(x=True, y=True)
        layout.addWidget(self.mood_stress_plot)
        
        # Water Intake Chart
        self.water_plot = pg.PlotWidget(title="Water Intake")
        self.water_plot.setLabel('left', 'Liters')
        self.water_plot.setLabel('bottom', 'Date')
        self.water_plot.showGrid(x=True, y=True)
        layout.addWidget(self.water_plot)
        
        widget.setLayout(layout)
        return widget
        
    def create_activity_tab(self):
        """Create physical activity charts tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Weight Chart
        self.weight_plot = pg.PlotWidget(title="Weight Trends")
        self.weight_plot.setLabel('left', 'Weight', units='kg')
        self.weight_plot.setLabel('bottom', 'Date')
        self.weight_plot.showGrid(x=True, y=True)
        layout.addWidget(self.weight_plot)
        
        # Steps Chart
        self.steps_plot = pg.PlotWidget(title="Daily Steps")
        self.steps_plot.setLabel('left', 'Steps')
        self.steps_plot.setLabel('bottom', 'Date')
        self.steps_plot.showGrid(x=True, y=True)
        layout.addWidget(self.steps_plot)
        
        # Exercise Chart
        self.exercise_plot = pg.PlotWidget(title="Exercise Duration")
        self.exercise_plot.setLabel('left', 'Minutes')
        self.exercise_plot.setLabel('bottom', 'Date')
        self.exercise_plot.showGrid(x=True, y=True)
        layout.addWidget(self.exercise_plot)
        
        widget.setLayout(layout)
        return widget
        
    def on_period_changed(self):
        """Handle time period change"""
        self.load_data()
        
    def get_days_for_period(self):
        """Get number of days based on selected period"""
        period_map = {
            "Last 7 days": 7,
            "Last 30 days": 30,
            "Last 90 days": 90,
            "Last 180 days": 180
        }
        return period_map.get(self.period_combo.currentText(), 30)
        
    def load_data(self):
        """Load chart data from API"""
        try:
            days = self.get_days_for_period()
            response = requests.get(
                f"{self.api_base_url}/api/v1/healthdata/charts?days={days}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.chart_data = response.json()
                self.update_charts()
            else:
                print(f"API Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}")
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def parse_dates(self, date_strings):
        """Convert date strings to timestamps for plotting"""
        timestamps = []
        for date_str in date_strings:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                timestamps.append(dt.timestamp())
            except ValueError:
                continue
        return np.array(timestamps)
        
    def filter_valid_data(self, dates, values):
        """Filter out None values and return valid data points"""
        valid_indices = [i for i, v in enumerate(values) if v is not None]
        valid_dates = [dates[i] for i in valid_indices]
        valid_values = [values[i] for i in valid_indices]
        return valid_dates, valid_values
        
    def update_charts(self):
        """Update all charts with loaded data"""
        if not self.chart_data:
            return
            
        dates = self.chart_data.get('dates', [])
        
        # Clear all plots
        self.bp_plot.clear()
        self.bs_plot.clear()
        self.hr_plot.clear()
        self.sleep_plot.clear()
        self.mood_stress_plot.clear()
        self.water_plot.clear()
        self.weight_plot.clear()
        self.steps_plot.clear()
        self.exercise_plot.clear()
        
        # Update Blood Pressure Chart
        systolic_data = self.chart_data.get('blood_pressure_systolic', [])
        diastolic_data = self.chart_data.get('blood_pressure_diastolic', [])
        
        systolic_dates, systolic_values = self.filter_valid_data(dates, systolic_data)
        diastolic_dates, diastolic_values = self.filter_valid_data(dates, diastolic_data)
        
        if systolic_values:
            systolic_x = self.parse_dates(systolic_dates)
            self.bp_plot.plot(systolic_x, systolic_values, pen=pg.mkPen('r', width=2), 
                             symbol='o', symbolBrush='r', symbolSize=6, name='Systolic')
            
        if diastolic_values:
            diastolic_x = self.parse_dates(diastolic_dates)
            self.bp_plot.plot(diastolic_x, diastolic_values, pen=pg.mkPen('b', width=2),
                             symbol='s', symbolBrush='b', symbolSize=6, name='Diastolic')
        
        # Update Blood Sugar Chart
        bs_dates, bs_values = self.filter_valid_data(dates, self.chart_data.get('blood_sugar', []))
        if bs_values:
            bs_x = self.parse_dates(bs_dates)
            self.bs_plot.plot(bs_x, bs_values, pen=pg.mkPen('g', width=2),
                             symbol='o', symbolBrush='g', symbolSize=6)
        
        # Update Heart Rate Chart (if available in future data)
        # hr_dates, hr_values = self.filter_valid_data(dates, self.chart_data.get('heart_rate', []))
        
        # Update Sleep Chart
        sleep_dates, sleep_values = self.filter_valid_data(dates, self.chart_data.get('sleep_hours', []))
        if sleep_values:
            sleep_x = self.parse_dates(sleep_dates)
            self.sleep_plot.plot(sleep_x, sleep_values, pen=pg.mkPen('purple', width=2),
                                symbol='o', symbolBrush='purple', symbolSize=8)
        
        # Update Mood & Stress Chart
        mood_dates, mood_values = self.filter_valid_data(dates, self.chart_data.get('mood_score', []))
        stress_dates, stress_values = self.filter_valid_data(dates, self.chart_data.get('stress_level', []))
        
        if mood_values:
            mood_x = self.parse_dates(mood_dates)
            self.mood_stress_plot.plot(mood_x, mood_values, pen=pg.mkPen('y', width=2),
                                      symbol='o', symbolBrush='y', symbolSize=6, name='Mood')
        
        if stress_values:
            stress_x = self.parse_dates(stress_dates)
            self.mood_stress_plot.plot(stress_x, stress_values, pen=pg.mkPen('r', width=2),
                                      symbol='s', symbolBrush='r', symbolSize=6, name='Stress')
        
        # Update Weight Chart
        weight_dates, weight_values = self.filter_valid_data(dates, self.chart_data.get('weight', []))
        if weight_values:
            weight_x = self.parse_dates(weight_dates)
            self.weight_plot.plot(weight_x, weight_values, pen=pg.mkPen('darkgreen', width=2),
                                 symbol='o', symbolBrush='darkgreen', symbolSize=6)
        
        # Format x-axis to show dates
        self.format_date_axis()
        
    def format_date_axis(self):
        """Format x-axis to show dates properly"""
        plots = [self.bp_plot, self.bs_plot, self.hr_plot, self.sleep_plot, 
                self.mood_stress_plot, self.water_plot, self.weight_plot, 
                self.steps_plot, self.exercise_plot]
        
        for plot in plots:
            axis = plot.getAxis('bottom')
            axis.setStyle(tickTextOffset=10)

# Fallback simple chart widget if PyQtGraph is not available
class SimpleHealthDataCharts(QWidget):
    """Simple text-based health data display"""
    
    def __init__(self, api_base_url="http://localhost:8000"):
        super().__init__()
        self.api_base_url = api_base_url
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        refresh_btn = QPushButton("Load Health Data Summary")
        refresh_btn.clicked.connect(self.load_summary)
        layout.addWidget(refresh_btn)
        
        self.summary_label = QLabel("Click 'Load Health Data Summary' to view your health statistics")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 15px;
                font-family: monospace;
            }
        """)
        
        layout.addWidget(self.summary_label)
        self.setLayout(layout)
        
    def load_summary(self):
        """Load and display health data summary"""
        try:
            response = requests.get(f"{self.api_base_url}/api/v1/healthdata/summary", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.display_summary(data)
            else:
                self.summary_label.setText(f"Error loading data: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.summary_label.setText(f"Network Error: {str(e)}")
        except Exception as e:
            self.summary_label.setText(f"Error: {str(e)}")
            
    def display_summary(self, data):
        """Display health data summary"""
        summary_text = "HEALTH DATA SUMMARY\n" + "="*50 + "\n\n"
        
        # Total entries
        summary_text += f"Total Entries: {data.get('total_entries', 0)}\n\n"
        
        # Date range
        date_range = data.get('date_range', {})
        if date_range.get('earliest'):
            summary_text += f"Data Range: {date_range.get('earliest')} to {date_range.get('latest')}\n\n"
        
        # Averages
        averages = data.get('averages', {})
        if averages:
            summary_text += "AVERAGE VALUES:\n" + "-"*20 + "\n"
            for key, value in averages.items():
                if value is not None:
                    unit = self.get_unit_for_metric(key)
                    summary_text += f"{key.replace('_', ' ').title()}: {value} {unit}\n"
            summary_text += "\n"
        
        # Latest readings
        latest = data.get('latest_readings', {})
        if latest:
            summary_text += "LATEST READINGS:\n" + "-"*20 + "\n"
            for key, value in latest.items():
                if value is not None and key != 'measurement_time':
                    unit = self.get_unit_for_metric(key)
                    summary_text += f"{key.replace('_', ' ').title()}: {value} {unit}\n"
            
            if latest.get('measurement_time'):
                summary_text += f"Recorded: {latest['measurement_time']}\n"
        
        self.summary_label.setText(summary_text)
        
    def get_unit_for_metric(self, metric):
        """Get appropriate unit for health metric"""
        units = {
            'systolic_bp': 'mmHg',
            'diastolic_bp': 'mmHg',
            'blood_sugar': 'mg/dL',
            'weight': 'kg',
            'heart_rate': 'bpm',
            'sleep_hours': 'hours',
            'water_intake': 'liters',
            'exercise_minutes': 'minutes'
        }
        return units.get(metric, '')

# Try to use PyQtGraph, fall back to simple charts if not available
try:
    import pyqtgraph as pg
    HealthDataVisualization = HealthDataCharts
except ImportError:
    print("PyQtGraph not available, using simple charts")
    HealthDataVisualization = SimpleHealthDataCharts