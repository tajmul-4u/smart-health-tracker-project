from PyQt6.QtWidgets import (QMainWindow, QTableWidgetItem, QMessageBox, 
                             QProgressBar, QMenu, QListWidgetItem, QVBoxLayout, 
                             QWidget, QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction
from PyQt6 import uic
from app.services.api_client import APIClient
import os
from datetime import datetime

class EnhancedDashboardController(QMainWindow):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.current_user = None
        
        # Load Enhanced UI
        ui_path = os.path.join(os.path.dirname(__file__), '../ui/enhanced_dashboard.ui')
        uic.loadUi(ui_path, self)
        
        # Initialize navigation
        self.setup_navigation()
        
        # Initialize notifications
        self.setup_notifications()
        
        # Initialize profile section
        self.setup_profile_section()
        
        # Load initial data
        self.load_user_data()
        self.load_dashboard_data()
        
        # Set default page
        self.contentStackedWidget.setCurrentIndex(0)  # Dashboard page
        
    def setup_navigation(self):
        """Setup left navigation menu connections"""
        # Connect navigation buttons
        self.dashboardNavButton.clicked.connect(lambda: self.switch_page(0))
        self.habitsNavButton.clicked.connect(lambda: self.switch_page(1))
        self.healthConditionsNavButton.clicked.connect(lambda: self.switch_page(2))
        self.analyticsNavButton.clicked.connect(lambda: self.switch_page(3))
        self.aiPredictionsNavButton.clicked.connect(lambda: self.switch_page(4))
        self.communityNavButton.clicked.connect(lambda: self.switch_page(5))
        self.settingsNavButton.clicked.connect(lambda: self.switch_page(6))
        self.logoutNavButton.clicked.connect(self.logout)
        
    def setup_notifications(self):
        """Setup notification system"""
        self.notificationButton.clicked.connect(self.show_notifications)
        
        # Sample notifications (in real app, fetch from backend)
        self.notifications = [
            {"type": "health_alert", "message": "Time for your evening medication", "time": "5 mins ago"},
            {"type": "achievement", "message": "You've reached your daily step goal!", "time": "2 hours ago"},
            {"type": "reminder", "message": "Don't forget to log your blood pressure", "time": "1 day ago"}
        ]
        
        # Update notification count
        self.update_notification_badge()
        
    def setup_profile_section(self):
        """Setup profile dropdown and actions"""
        self.profileDropdownButton.clicked.connect(self.show_profile_menu)
        
    def switch_page(self, page_index):
        """Switch between different pages in the stacked widget"""
        self.contentStackedWidget.setCurrentIndex(page_index)
        
        # Update page-specific data based on selection
        if page_index == 0:  # Dashboard
            self.refresh_dashboard()
        elif page_index == 1:  # Habits
            self.refresh_habits()
        elif page_index == 2:  # Health Conditions
            self.refresh_health_conditions()
        elif page_index == 3:  # Analytics
            self.refresh_analytics()
        elif page_index == 4:  # AI Predictions
            self.refresh_ai_predictions()
        elif page_index == 5:  # Community
            self.refresh_community()
        elif page_index == 6:  # Settings
            self.refresh_settings()
            
    def load_user_data(self):
        """Load current user data"""
        try:
            self.current_user = self.api_client.get_current_user()
            self.userNameLabel.setText(self.current_user.get('full_name', 'User'))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load user data: {str(e)}")
            self.userNameLabel.setText("Guest User")
            
    def load_dashboard_data(self):
        """Load dashboard overview data"""
        try:
            # Load recent activities from API
            self.load_recent_activities()
            
            # Update quick stats from API
            self.update_quick_stats()
            
            # Load notifications
            self.load_notifications()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load dashboard data: {str(e)}")
            
    def load_recent_activities(self):
        """Load recent activities list from API"""
        try:
            activities = self.api_client.get_recent_activities()
            self.recentActivitiesList.clear()
            
            for activity in activities:
                activity_text = f"{activity['activity']} - {activity['time']}"
                item = QListWidgetItem(activity_text)
                self.recentActivitiesList.addItem(item)
                
        except Exception as e:
            # Fallback to sample data
            activities = [
                "🚶 Walked 8,450 steps today",
                "😴 Slept 7.5 hours last night", 
                "💧 Drank 2.1L water today",
                "🍎 Logged breakfast: Oatmeal with fruits",
                "💊 Took morning medication",
                "🧘 Completed 10-minute meditation",
                "📊 Blood pressure recorded: 120/80"
            ]
            
            self.recentActivitiesList.clear()
            for activity in activities:
                item = QListWidgetItem(activity)
                self.recentActivitiesList.addItem(item)
            
    def update_quick_stats(self):
        """Update quick stats cards with current data from API"""
        try:
            stats = self.api_client.get_health_stats()
            
            # Update stat cards with real data
            self.statCard1Value.setText(f"{stats['steps']:,}")
            self.statCard2Value.setText(f"{stats['sleep_hours']}h")
            self.statCard3Value.setText(f"{stats['water_intake']}L")
            self.statCard4Value.setText(f"{stats['mood_score']}/10")
            
        except Exception as e:
            # Keep default values if API fails
            print(f"Failed to load health stats: {str(e)}")
            
    def load_notifications(self):
        """Load notifications from API"""
        try:
            self.notifications = self.api_client.get_notifications()
            self.update_notification_badge()
        except Exception as e:
            # Use fallback notifications
            self.notifications = [
                {"type": "health_alert", "message": "Time for your evening medication", "time": "5 mins ago"},
                {"type": "achievement", "message": "You've reached your daily step goal!", "time": "2 hours ago"},
                {"type": "reminder", "message": "Don't forget to log your blood pressure", "time": "1 day ago"}
            ]
            self.update_notification_badge()
        
    def show_notifications(self):
        """Show notifications dropdown"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                min-width: 300px;
            }
            QMenu::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QMenu::item:hover {
                background-color: #f0f0f0;
            }
        """)
        
        if not self.notifications:
            action = QAction("No new notifications", self)
            action.setEnabled(False)
            menu.addAction(action)
        else:
            for notification in self.notifications:
                action_text = f"{notification['message']}\n{notification['time']}"
                action = QAction(action_text, self)
                menu.addAction(action)
                
        # Show menu below the notification button
        button_rect = self.notificationButton.geometry()
        menu.exec(self.notificationButton.mapToGlobal(button_rect.bottomLeft()))
        
    def update_notification_badge(self):
        """Update notification badge count"""
        count = len(self.notifications)
        if count > 0:
            self.notificationButton.setText(f"🔔 {count}")
        else:
            self.notificationButton.setText("🔔")
            
    def show_profile_menu(self):
        """Show profile dropdown menu"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                min-width: 150px;
            }
            QMenu::item {
                padding: 8px 16px;
            }
            QMenu::item:hover {
                background-color: #f0f0f0;
            }
        """)
        
        # Profile actions
        profile_action = QAction("👤 View Profile", self)
        profile_action.triggered.connect(self.show_profile_settings)
        menu.addAction(profile_action)
        
        settings_action = QAction("⚙️ Settings", self)
        settings_action.triggered.connect(lambda: self.switch_page(6))
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        logout_action = QAction("🚪 Logout", self)
        logout_action.triggered.connect(self.logout)
        menu.addAction(logout_action)
        
        # Show menu below the profile section
        profile_rect = self.profileSection.geometry()
        menu.exec(self.profileSection.mapToGlobal(profile_rect.bottomLeft()))
        
    def show_profile_settings(self):
        """Show profile settings dialog"""
        # Switch to settings page for now
        self.switch_page(6)
        
    def refresh_dashboard(self):
        """Refresh dashboard page data"""
        self.load_recent_activities()
        self.update_quick_stats()
        
    def refresh_habits(self):
        """Refresh habits page data"""
        # Load habits data from backend
        try:
            habits = self.api_client.get_habits()
            # Update habits display
            # Implementation depends on specific habits UI components
        except Exception as e:
            print(f"Failed to load habits: {str(e)}")
            
    def refresh_health_conditions(self):
        """Refresh health conditions page data"""
        # Load health conditions data
        print("Loading health conditions data...")
        
    def refresh_analytics(self):
        """Refresh analytics page data"""
        # Load analytics and charts
        print("Loading analytics data...")
        
    def refresh_ai_predictions(self):
        """Refresh AI predictions page data"""
        # Load AI predictions
        print("Loading AI predictions...")
        
    def refresh_community(self):
        """Refresh community insights page data"""
        # Load community data
        print("Loading community insights...")
        
    def refresh_settings(self):
        """Refresh settings page"""
        print("Loading settings...")
        
    def logout(self):
        """Handle user logout"""
        reply = QMessageBox.question(
            self, 
            "Logout", 
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear user session data
            self.current_user = None
            
            # Close dashboard and return to login
            self.close()
            
            # Show success message
            QMessageBox.information(self, "Logout", "You have been logged out successfully!")
            
    def closeEvent(self, event):
        """Handle window close event"""
        # Save any pending data before closing
        event.accept()