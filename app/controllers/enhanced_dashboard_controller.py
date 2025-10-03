from PyQt6.QtWidgets import (QMainWindow, QTableWidgetItem, QMessageBox, 
                             QProgressBar, QMenu, QListWidgetItem, QVBoxLayout, 
                             QWidget, QLabel, QHBoxLayout, QDialog, QPushButton)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QFont
from PyQt6 import uic
from app.services.api_client import APIClient
from app.widgets.health_data_widget import HealthDataInputWidget
from app.widgets.user_profile_form import UserProfileFormWidget
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
        try:
            # Connect dropdown button
            self.profileDropdownButton.clicked.connect(self.show_profile_menu)
            
            # Make profile icon and name clickable
            if hasattr(self, 'userAvatarLabel'):
                self.userAvatarLabel.mousePressEvent = lambda event: self.show_profile_menu()
                self.userAvatarLabel.setStyleSheet(
                    self.userAvatarLabel.styleSheet() + 
                    "; cursor: pointer; border-radius: 15px;"
                )
                self.userAvatarLabel.setToolTip("Click to access profile menu")
                
            if hasattr(self, 'userNameLabel'):
                self.userNameLabel.mousePressEvent = lambda event: self.show_profile_menu()
                self.userNameLabel.setStyleSheet(
                    self.userNameLabel.styleSheet() + 
                    "; cursor: pointer;"
                )
                self.userNameLabel.setToolTip("Click to access profile menu")
                
        except AttributeError:
            # If UI elements don't exist, create profile functionality programmatically
            pass
            
    def show_profile_menu(self):
        """Show profile dropdown menu with profile form prioritized"""
        menu = QMenu(self)
        
        # Profile Form Action (Primary)
        profile_form_action = QAction("👤 Edit Profile", self)
        profile_form_action.triggered.connect(self.show_profile_form)
        profile_form_action.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        menu.addAction(profile_form_action)
        
        menu.addSeparator()
        
        # Health Data Input Action
        health_data_action = QAction("🏥 Health Data", self)
        health_data_action.triggered.connect(self.show_health_data_input)
        menu.addAction(health_data_action)
        
        # View Profile Info (Quick View)
        view_profile_action = QAction("📋 View Profile Info", self)
        view_profile_action.triggered.connect(self.show_profile_info)
        menu.addAction(view_profile_action)
        
        menu.addSeparator()
        
        # Settings Action
        settings_action = QAction("⚙️ Settings", self)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)
        
        # Logout Action
        logout_action = QAction("🚪 Logout", self)
        logout_action.triggered.connect(self.logout)
        menu.addAction(logout_action)
        
        # Show menu at button position
        try:
            menu.exec(self.profileDropdownButton.mapToGlobal(self.profileDropdownButton.rect().bottomLeft()))
        except AttributeError:
            menu.exec(self.mapToGlobal(self.rect().topRight()))
            
    def show_profile_form(self):
        """Show comprehensive user profile form"""
        dialog = QDialog(self)
        dialog.setWindowTitle("👤 User Profile Management")
        dialog.setModal(True)
        dialog.resize(900, 700)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add user profile form widget
        profile_form = UserProfileFormWidget(self.api_client)
        
        # Connect signals
        profile_form.profile_saved.connect(self.on_profile_saved)
        profile_form.profile_updated.connect(self.on_profile_updated)
        
        layout.addWidget(profile_form)
        
        # Add close button
        close_button = QPushButton("✅ Close")
        close_button.clicked.connect(dialog.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(close_button)
        
        dialog.setLayout(layout)
        dialog.exec()
        
    def on_profile_saved(self, profile_data):
        """Handle profile save events"""
        try:
            # Update the user name label if available
            if hasattr(self, 'userNameLabel'):
                self.userNameLabel.setText(profile_data.get('full_name', 'User'))
                
            # Update current user data
            self.current_user = profile_data
            
            # Show success message
            QMessageBox.information(
                self,
                "✅ Profile Saved",
                f"Profile information saved successfully!\n\n"
                f"Name: {profile_data.get('full_name', 'N/A')}\n"
                f"Email: {profile_data.get('email', 'N/A')}\n"
                f"Phone: {profile_data.get('phone', 'N/A')}"
            )
            
            # Refresh dashboard data
            self.load_dashboard_data()
            
        except Exception as e:
            print(f"Error handling profile save: {e}")
            
    def on_profile_updated(self, profile_data):
        """Handle profile update events"""
        try:
            # Update the user name label if available
            if hasattr(self, 'userNameLabel'):
                self.userNameLabel.setText(profile_data.get('full_name', 'User'))
                
            # Update current user data
            if isinstance(profile_data, dict):
                if not hasattr(self, 'current_user') or self.current_user is None:
                    self.current_user = {}
                self.current_user.update(profile_data)
                
            print(f"Profile updated: {profile_data.get('full_name', 'Unknown')}")
            
        except Exception as e:
            print(f"Error handling profile update: {e}")
            
    def show_health_data_input(self):
        """Show health data input dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("🏥 Health Data Input - Profile Section")
        dialog.setModal(True)
        dialog.resize(800, 600)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add health data widget
        health_widget = HealthDataInputWidget(self.api_client)
        
        # Connect signals
        health_widget.data_updated.connect(self.on_health_data_updated)
        health_widget.user_profile_changed.connect(self.on_user_profile_changed)
        
        layout.addWidget(health_widget)
        
        # Add close button
        close_button = QPushButton("✅ Done")
        close_button.clicked.connect(dialog.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(close_button)
        
        dialog.setLayout(layout)
        dialog.exec()
        
    def show_profile_info(self):
        """Show user profile information"""
        try:
            user_data = self.api_client.get_current_user() if self.api_client else self.current_user
            
            info_text = f"""
👤 User Profile Information

📧 Email: {user_data.get('email', 'Not set')}
👤 Username: {user_data.get('username', 'Not set')} 
📛 Full Name: {user_data.get('full_name', 'Not set')}
🎂 Age: {user_data.get('age', 'Not set')} years
⚥ Gender: {user_data.get('gender', 'Not set')}
📏 Height: {user_data.get('height', 'Not set')} cm
⚖️ Weight: {user_data.get('weight', 'Not set')} kg

Click 'Update Health Data' to modify your health information.
            """
            
            QMessageBox.information(self, "👤 Profile Information", info_text)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load profile: {str(e)}")
            
    def on_health_data_updated(self, health_summary):
        """Handle health data updates from the widget"""
        try:
            # Update dashboard with new health data
            self.refresh_dashboard()
            
            # Show confirmation
            QMessageBox.information(
                self,
                "✅ Health Data Updated",
                f"Your health data has been updated!\n\n"
                f"Latest readings:\n"
                f"• Blood Pressure: {health_summary.get('blood_pressure', 'N/A')}\n"
                f"• Blood Sugar: {health_summary.get('blood_sugar', 'N/A')} mg/dL\n"
                f"• Sleep: {health_summary.get('sleep_hours', 'N/A')} hours\n"
                f"• Steps: {health_summary.get('steps', 'N/A')}\n"
                f"• Mood: {health_summary.get('mood_score', 'N/A')}/10"
            )
            
        except Exception as e:
            print(f"Error updating dashboard: {e}")
            
    def on_user_profile_changed(self, profile_data):
        """Handle user profile changes from the widget"""
        try:
            # Update current user data
            if hasattr(self, 'current_user'):
                self.current_user.update(profile_data)
                
            # Update UI if elements exist
            if hasattr(self, 'userNameLabel'):
                self.userNameLabel.setText(profile_data.get('full_name', 'User'))
                
        except Exception as e:
            print(f"Error updating user profile: {e}")
            
    def show_settings(self):
        """Show settings dialog"""
        QMessageBox.information(
            self,
            "⚙️ Settings",
            "Settings panel would be displayed here.\n\n"
            "Available settings:\n"
            "• Notification preferences\n"
            "• Data export/import\n"
            "• Privacy settings\n"
            "• App preferences"
        )
        
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