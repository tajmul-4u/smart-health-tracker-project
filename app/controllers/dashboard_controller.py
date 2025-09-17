from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QProgressBar
from PyQt6 import uic
from app.services.api_client import APIClient
import os

class DashboardController(QMainWindow):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        
        # Load UI
        ui_path = os.path.join(os.path.dirname(__file__), '../ui/dashboard.ui')
        uic.loadUi(ui_path, self)
        
        # Connect signals
        self.addHabitButton.clicked.connect(self.show_add_habit_dialog)
        self.generateRecommendationsButton.clicked.connect(self.generate_recommendations)
        self.updateProfileButton.clicked.connect(self.update_profile)
        
        # Initialize UI
        self.load_user_profile()
        self.load_habits()
        self.load_recommendations()
        
    def load_user_profile(self):
        try:
            user_data = self.api_client.get_current_user()
            self.usernameInput.setText(user_data['username'])
            self.fullNameInput.setText(user_data.get('full_name', ''))
            self.ageSpinBox.setValue(user_data.get('age', 0))
            self.weightSpinBox.setValue(user_data.get('weight', 0.0))
            self.heightSpinBox.setValue(user_data.get('height', 0.0))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load profile: {str(e)}")
            
    def load_habits(self):
        try:
            habits = self.api_client.get_habits()
            self.habitsTable.setRowCount(len(habits))
            
            for row, habit in enumerate(habits):
                self.habitsTable.setItem(row, 0, QTableWidgetItem(habit['name']))
                
                # Create progress bar
                progress = QProgressBar()
                progress.setMaximum(int(habit['target_value']))
                progress.setValue(int(habit['current_value']))
                self.habitsTable.setCellWidget(row, 1, progress)
                
                self.habitsTable.setItem(row, 2, QTableWidgetItem(str(habit['target_value'])))
                self.habitsTable.setItem(row, 3, QTableWidgetItem(habit['unit']))
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load habits: {str(e)}")
            
    def load_recommendations(self):
        try:
            recommendations = self.api_client.get_recommendations()
            self.recommendationsList.clear()
            
            for rec in recommendations:
                self.recommendationsList.addItem(
                    f"{rec['title']} (Priority: {rec['priority_level']})\n"
                    f"{rec['description']}"
                )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load recommendations: {str(e)}")
            
    def show_add_habit_dialog(self):
        # This will be implemented when we create the add habit dialog
        pass
        
    def generate_recommendations(self):
        try:
            recommendations = self.api_client.generate_recommendations()
            self.load_recommendations()
            QMessageBox.information(self, "Success", "New recommendations generated!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to generate recommendations: {str(e)}")
            
    def update_profile(self):
        try:
            user_data = {
                'full_name': self.fullNameInput.text(),
                'age': self.ageSpinBox.value(),
                'weight': self.weightSpinBox.value(),
                'height': self.heightSpinBox.value()
            }
            self.api_client.update_user(user_data)
            QMessageBox.information(self, "Success", "Profile updated successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update profile: {str(e)}")
