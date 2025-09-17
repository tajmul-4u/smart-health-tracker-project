import requests
from typing import Dict, List, Optional
from ..utils.config import API_URL

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