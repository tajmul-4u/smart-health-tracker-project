#!/usr/bin/env python3
"""
Modern Health Input System Demo
Showcase of the enhanced user-friendly health data management system
"""

import sys
import os
sys.path.insert(0, '/home/tajmul/Projects/Python/health-recomand/smart_health_tracker')

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLabel, QFrame, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QBrush, QPalette

from app.widgets.modern_health_input import ModernHealthDataInput

class ModernHealthDemo(QMainWindow):
    """Demo application for the modern health input system"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_demo_data()
        
    def init_ui(self):
        """Initialize the demo interface"""
        self.setWindowTitle("🏥 Modern Health Input System - Demo & Showcase")
        self.setGeometry(50, 50, 1400, 1000)
        
        # Set modern window style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QLabel {
                color: #2c3e50;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
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
        
        # Central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create splitter for side panel and main content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side panel
        side_panel = self.create_side_panel()
        splitter.addWidget(side_panel)
        
        # Main content area
        self.main_content = QWidget()
        self.create_main_content()
        splitter.addWidget(self.main_content)
        
        # Set splitter proportions
        splitter.setSizes([400, 1000])
        
        main_layout.addWidget(splitter)
        
    def create_side_panel(self):
        """Create side panel with demo information"""
        panel = QFrame()
        panel.setFixedWidth(400)
        panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-right: 2px solid #dee2e6;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Title
        title = QLabel("🏥 Modern Health Input")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #007bff; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Description
        description = QLabel("""
<h3>🎯 Enhanced Features:</h3>
<ul>
<li><b>⚡ Quick Input Mode:</b> Fast data entry with smart sliders and visual feedback</li>
<li><b>📋 Detailed Forms:</b> Comprehensive health data collection with validation</li>
<li><b>📈 Visual Trends:</b> Chart integration and progress tracking</li>
<li><b>🤖 Smart Validation:</b> Real-time input validation and suggestions</li>
<li><b>💾 Auto-Save:</b> Automatic data persistence and offline support</li>
<li><b>🎨 Modern UI:</b> Professional design with animations and effects</li>
</ul>

<h3>🚀 User Experience Improvements:</h3>
<ul>
<li><b>Intuitive Navigation:</b> Tabbed interface for organized data entry</li>
<li><b>Visual Feedback:</b> Color-coded sliders and progress indicators</li>
<li><b>Smart Cards:</b> Quick input cards for common metrics</li>
<li><b>Contextual Help:</b> Tooltips and guidance throughout</li>
<li><b>Responsive Design:</b> Adapts to different screen sizes</li>
</ul>

<h3>⚙️ Technical Features:</h3>
<ul>
<li><b>Real-time API Integration:</b> Immediate data synchronization</li>
<li><b>Form Validation:</b> Prevents invalid data entry</li>
<li><b>Offline Support:</b> Local data storage when offline</li>
<li><b>Animation System:</b> Smooth transitions and feedback</li>
<li><b>Accessibility:</b> Keyboard navigation and screen reader support</li>
</ul>
        """)
        description.setWordWrap(True)
        description.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
                color: #495057;
                line-height: 1.4;
            }
        """)
        layout.addWidget(description)
        
        # Demo buttons
        buttons_layout = QVBoxLayout()
        
        # Quick demo button
        quick_demo_btn = QPushButton("⚡ Quick Input Demo")
        quick_demo_btn.clicked.connect(self.show_quick_demo)
        quick_demo_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #1e7e34);
                margin: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34ce57, stop:1 #28a745);
            }
        """)
        buttons_layout.addWidget(quick_demo_btn)
        
        # Full demo button
        full_demo_btn = QPushButton("📋 Full System Demo")
        full_demo_btn.clicked.connect(self.show_full_demo)
        full_demo_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                margin: 5px;
            }
        """)
        buttons_layout.addWidget(full_demo_btn)
        
        # API test button
        api_test_btn = QPushButton("🔗 Test API Connection")
        api_test_btn.clicked.connect(self.test_api_connection)
        api_test_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffc107, stop:1 #e0a800);
                color: #212529;
                margin: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffcd39, stop:1 #ffc107);
            }
        """)
        buttons_layout.addWidget(api_test_btn)
        
        # Reset demo button
        reset_btn = QPushButton("🔄 Reset Demo")
        reset_btn.clicked.connect(self.reset_demo)
        reset_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #545b62);
                margin: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7c848b, stop:1 #6c757d);
            }
        """)
        buttons_layout.addWidget(reset_btn)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        # Status information
        status_label = QLabel("💡 Click any demo button to start exploring!")
        status_label.setStyleSheet("""
            QLabel {
                background-color: #e7f3ff;
                border: 1px solid #007bff;
                border-radius: 6px;
                padding: 10px;
                color: #004085;
                font-weight: bold;
                text-align: center;
            }
        """)
        layout.addWidget(status_label)
        
        return panel
        
    def create_main_content(self):
        """Create main content area"""
        layout = QVBoxLayout()
        self.main_content.setLayout(layout)
        
        # Welcome message
        welcome = QLabel("🎉 Welcome to the Modern Health Input System Demo!")
        welcome.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007bff, stop:1 #0056b3);
                color: white;
                padding: 30px;
                border-radius: 12px;
                margin: 20px;
            }
        """)
        layout.addWidget(welcome)
        
        # Demo content placeholder
        self.demo_content = QLabel("""
<div style="text-align: center; padding: 50px;">
<h2>🚀 Ready to Explore?</h2>
<p style="font-size: 18px; color: #6c757d; line-height: 1.6;">
Select a demo option from the left panel to see the modern health input system in action.
</p>

<h3>✨ What Makes This System Special:</h3>
<div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
<p><b>🎯 User-Centric Design:</b> Built with user experience as the top priority</p>
<p><b>⚡ Performance Optimized:</b> Fast, responsive, and efficient data handling</p>
<p><b>🔒 Secure & Private:</b> Your health data is protected and encrypted</p>
<p><b>📱 Future-Ready:</b> Designed for scalability and future enhancements</p>
</div>

<p style="font-size: 16px; color: #495057;">
This system represents the next generation of health data management,
combining modern UI design principles with practical functionality.
</p>
</div>
        """)
        self.demo_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.demo_content.setWordWrap(True)
        self.demo_content.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 12px;
                margin: 20px;
                padding: 20px;
            }
        """)
        layout.addWidget(self.demo_content)
        
    def setup_demo_data(self):
        """Setup demo data and connections"""
        self.demo_active = False
        
        # Setup timer for demo updates
        self.demo_timer = QTimer()
        self.demo_timer.timeout.connect(self.update_demo_status)
        
    def show_quick_demo(self):
        """Show quick input demo"""
        try:
            # Create modern health input widget with focus on quick input
            health_widget = ModernHealthDataInput()
            
            # Create demo dialog
            dialog = self.create_demo_dialog("⚡ Quick Input Demo", health_widget)
            
            # Set to quick input tab
            health_widget.tab_widget.setCurrentIndex(0)
            
            # Connect demo signals
            health_widget.data_submitted.connect(self.on_demo_data_submitted)
            health_widget.data_updated.connect(self.on_demo_data_updated)
            
            # Show dialog
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Demo Error", f"Could not start quick demo: {str(e)}")
            
    def show_full_demo(self):
        """Show full system demo"""
        try:
            # Create modern health input widget
            health_widget = ModernHealthDataInput()
            
            # Create demo dialog
            dialog = self.create_demo_dialog("📋 Full System Demo", health_widget)
            
            # Connect demo signals
            health_widget.data_submitted.connect(self.on_demo_data_submitted)
            health_widget.data_updated.connect(self.on_demo_data_updated)
            health_widget.validation_failed.connect(self.on_demo_validation_failed)
            
            # Show dialog
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Demo Error", f"Could not start full demo: {str(e)}")
            
    def create_demo_dialog(self, title, widget):
        """Create demo dialog with consistent styling"""
        from PyQt6.QtWidgets import QDialog
        
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setModal(True)
        dialog.resize(1200, 900)
        
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        
        dialog.setLayout(layout)
        return dialog
        
    def test_api_connection(self):
        """Test API connection"""
        try:
            import requests
            
            # Test backend connection
            response = requests.get("http://localhost:8000/health", timeout=3)
            
            if response.status_code == 200:
                QMessageBox.information(
                    self, 
                    "✅ API Connection Successful",
                    "Backend API is running and accessible!\n\n"
                    "• Health endpoint: ✅ Working\n"
                    "• API status: ✅ Online\n"
                    "• Data sync: ✅ Ready\n\n"
                    "The modern health input system can now save data to the backend."
                )
            else:
                QMessageBox.warning(
                    self,
                    "⚠️ API Connection Issue", 
                    f"Backend responded with status {response.status_code}\n\n"
                    "The system will work in offline mode."
                )
                
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(
                self,
                "🔴 API Connection Failed",
                "Could not connect to the backend API.\n\n"
                "• Backend may not be running\n"
                "• Check if server is started\n"
                "• System will work in offline mode\n\n"
                f"Technical details: {str(e)[:100]}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error testing API: {str(e)}")
            
    def reset_demo(self):
        """Reset demo to initial state"""
        self.demo_content.setText("""
<div style="text-align: center; padding: 50px;">
<h2>🔄 Demo Reset Complete!</h2>
<p style="font-size: 18px; color: #6c757d; line-height: 1.6;">
The demo has been reset to its initial state. You can now explore all features again.
</p>

<h3>🎯 Ready for Another Round?</h3>
<div style="background: #e7f3ff; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #007bff;">
<p><b>⚡ Quick Input:</b> Try the fast data entry mode</p>
<p><b>📋 Full System:</b> Explore all comprehensive features</p>
<p><b>🔗 API Test:</b> Verify backend connectivity</p>
</div>

<p style="font-size: 16px; color: #495057;">
Each demo showcases different aspects of the modern health input system.
</p>
</div>
        """)
        
        self.demo_active = False
        
        QMessageBox.information(
            self,
            "✅ Reset Complete",
            "Demo has been reset successfully!\n\nYou can now start fresh with any demo option."
        )
        
    def on_demo_data_submitted(self, data):
        """Handle demo data submission"""
        self.demo_content.setText(f"""
<div style="text-align: center; padding: 30px;">
<h2>✅ Data Submitted Successfully!</h2>
<p style="font-size: 16px; color: #28a745; font-weight: bold;">
Health data has been processed and saved.
</p>

<div style="background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #28a745;">
<h3>📊 Submission Summary:</h3>
<p><b>Timestamp:</b> {data.get('timestamp', 'Unknown')}</p>
<p><b>Data Points:</b> {len([k for k, v in data.items() if v and k != 'timestamp'])}</p>
<p><b>Entry Type:</b> {data.get('entry_type', 'Manual entry')}</p>
</div>

<p style="font-size: 14px; color: #6c757d;">
In a real application, this data would be:\n
• Stored in the database\n
• Available for trend analysis\n
• Used for health insights\n
• Synchronized across devices
</p>
</div>
        """)
        
    def on_demo_data_updated(self, data):
        """Handle demo data updates"""
        if len(data) > 0:
            self.demo_content.setText(f"""
<div style="text-align: center; padding: 30px;">
<h2>🔄 Data Updated</h2>
<p style="font-size: 16px; color: #007bff;">
Form data is being updated in real-time.
</p>

<div style="background: #e7f3ff; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #007bff;">
<h3>📝 Current Data:</h3>
<p><b>Active Fields:</b> {len(data)} field(s) with data</p>
<p><b>Auto-save:</b> Enabled (saves after 2 seconds of inactivity)</p>
<p><b>Validation:</b> Real-time checking active</p>
</div>

<p style="font-size: 14px; color: #6c757d;">
The system provides instant feedback and validation as you type.
</p>
</div>
            """)
            
    def on_demo_validation_failed(self, error_message):
        """Handle demo validation failures"""
        self.demo_content.setText(f"""
<div style="text-align: center; padding: 30px;">
<h2>⚠️ Validation Demo</h2>
<p style="font-size: 16px; color: #dc3545;">
The validation system caught an issue.
</p>

<div style="background: #f8d7da; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #dc3545;">
<h3>🛡️ Validation Error:</h3>
<p><b>Message:</b> {error_message}</p>
<p><b>Prevention:</b> Invalid data entry blocked</p>
<p><b>User Guidance:</b> Clear error message provided</p>
</div>

<p style="font-size: 14px; color: #6c757d;">
This demonstrates how the system prevents invalid data\n
and guides users to correct their input.
</p>
</div>
        """)
        
    def update_demo_status(self):
        """Update demo status periodically"""
        # This could be used for live demo updates
        pass

def main():
    """Run the modern health input demo"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyleSheet("""
        QApplication {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
        }
    """)
    
    # Create and show demo window
    demo = ModernHealthDemo()
    demo.show()
    
    # Start the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()