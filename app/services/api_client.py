import requests
import sys
import os
from typing import Dict, List, Optional

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '../..')
sys.path.insert(0, project_root)

try:
    from app.utils.config import API_URL
except ImportError:
    from utils.config import API_URL

class APIClient:
    def __init__(self):
        self.base_url = API_URL
        self.token = None

    def _get_headers(self) -> Dict:
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def login(self, email: str, password: str) -> Dict:
        response = requests.post(
            f"{self.base_url}/api/users/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data['access_token']
            return data
        response.raise_for_status()

    def register(self, user_data: Dict) -> Dict:
        response = requests.post(
            f"{self.base_url}/api/users/register",
            json=user_data
        )
        response.raise_for_status()
        return response.json()

    def get_current_user(self) -> Dict:
        response = requests.get(
            f"{self.base_url}/api/users/me",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def update_user(self, user_data: Dict) -> Dict:
        response = requests.put(
            f"{self.base_url}/api/users/me",
            headers=self._get_headers(),
            json=user_data
        )
        response.raise_for_status()
        return response.json()

    def get_habits(self) -> List[Dict]:
        response = requests.get(
            f"{self.base_url}/api/habits",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def create_habit(self, habit_data: Dict) -> Dict:
        response = requests.post(
            f"{self.base_url}/api/habits",
            headers=self._get_headers(),
            json=habit_data
        )
        response.raise_for_status()
        return response.json()

    def update_habit(self, habit_id: int, habit_data: Dict) -> Dict:
        response = requests.put(
            f"{self.base_url}/api/habits/{habit_id}",
            headers=self._get_headers(),
            json=habit_data
        )
        response.raise_for_status()
        return response.json()

    def delete_habit(self, habit_id: int) -> None:
        response = requests.delete(
            f"{self.base_url}/api/habits/{habit_id}",
            headers=self._get_headers()
        )
        response.raise_for_status()

    def get_recommendations(self) -> List[Dict]:
        response = requests.get(
            f"{self.base_url}/api/recommendations",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def generate_recommendations(self) -> List[Dict]:
        response = requests.post(
            f"{self.base_url}/api/recommendations/generate",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def mark_recommendation_implemented(self, recommendation_id: int) -> Dict:
        response = requests.put(
            f"{self.base_url}/api/recommendations/{recommendation_id}/implement",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    # Health tracking methods
    def get_health_stats(self) -> Dict:
        """Get quick health statistics"""
        response = requests.get(
            f"{self.base_url}/api/health/stats",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def get_recent_activities(self) -> List[Dict]:
        """Get recent health activities"""
        response = requests.get(
            f"{self.base_url}/api/health/activities",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def get_notifications(self) -> List[Dict]:
        """Get user notifications"""
        response = requests.get(
            f"{self.base_url}/api/notifications",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def mark_notification_read(self, notification_id: int) -> Dict:
        """Mark notification as read"""
        response = requests.post(
            f"{self.base_url}/api/notifications/{notification_id}/read",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    # Health conditions methods
    def get_health_conditions(self) -> Dict:
        """Get health conditions data"""
        response = requests.get(
            f"{self.base_url}/api/health/conditions",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def log_blood_pressure(self, systolic: int, diastolic: int, date: Optional[str] = None) -> Dict:
        """Log blood pressure reading"""
        data = {"systolic": systolic, "diastolic": diastolic}
        if date:
            data["date"] = date
        
        response = requests.post(
            f"{self.base_url}/api/health/conditions/blood_pressure",
            headers=self._get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()

    def log_blood_sugar(self, level: float, meal_relation: str = "fasting", date: Optional[str] = None) -> Dict:
        """Log blood sugar reading"""
        data = {"level": level, "meal_relation": meal_relation}
        if date:
            data["date"] = date
            
        response = requests.post(
            f"{self.base_url}/api/health/conditions/blood_sugar",
            headers=self._get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()

    def log_stress_level(self, level: int, notes: str = "", date: Optional[str] = None) -> Dict:
        """Log stress level (1-10 scale)"""
        data = {"level": level, "notes": notes}
        if date:
            data["date"] = date
            
        response = requests.post(
            f"{self.base_url}/api/health/conditions/stress",
            headers=self._get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()

    # Analytics methods
    def get_health_trends(self) -> Dict:
        """Get health trends for analytics"""
        response = requests.get(
            f"{self.base_url}/api/analytics/trends",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    # Community methods
    def get_community_insights(self) -> Dict:
        """Get community health insights"""
        response = requests.get(
            f"{self.base_url}/api/community/insights",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    # Generic HTTP methods
    def get(self, endpoint: str) -> Optional[Dict]:
        """Generic GET request"""
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return None

    def post(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """Generic POST request"""
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                headers=self._get_headers(),
                json=data,
                timeout=5
            )
            if response.status_code in [200, 201]:
                return response.json()
        except Exception:
            pass
        return None