"""
Health Data API Demo Script
Demonstrates how to interact with the health data API endpoints
"""
import requests
import json
from datetime import datetime, date
from typing import Dict, Any

class HealthDataAPIClient:
    """Client for interacting with Health Data API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def submit_health_data(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit health data to the API"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/healthdata",
                json=health_data,
                timeout=10
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def get_health_data(self, limit: int = 10) -> Dict[str, Any]:
        """Get health data entries"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/healthdata?limit={limit}",
                timeout=10
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get health data summary"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/healthdata/summary",
                timeout=10
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def get_chart_data(self, days: int = 30) -> Dict[str, Any]:
        """Get chart data for visualization"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/healthdata/charts?days={days}",
                timeout=10
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

def demo_health_data_submission():
    """Demonstrate health data submission"""
    print("=" * 60)
    print("HEALTH DATA API DEMONSTRATION")
    print("=" * 60)
    
    # Initialize API client
    client = HealthDataAPIClient()
    
    # Sample health data
    sample_health_data = {
        "systolic_bp": 120.0,
        "diastolic_bp": 80.0,
        "blood_sugar": 95.0,
        "sugar_test_type": "fasting",
        "sleep_hours": 7.5,
        "sleep_quality": 8,
        "stress_level": 3,
        "stress_notes": "Feeling relaxed after morning exercise",
        "steps_count": 8500,
        "exercise_minutes": 30.0,
        "weight": 75.2,
        "height": 175.0,
        "heart_rate": 72,
        "water_intake": 2.1,
        "mood_score": 8,
        "energy_level": 7,
        "notes": "Good day overall, completed morning workout",
        "measurement_time": datetime.now().isoformat()
    }
    
    print("\n1. SUBMITTING HEALTH DATA")
    print("-" * 30)
    print("Sample data:")
    print(json.dumps(sample_health_data, indent=2))
    
    # Submit health data
    result = client.submit_health_data(sample_health_data)
    
    if result["success"]:
        print("\n✅ Health data submitted successfully!")
        print("Response:", json.dumps(result["data"], indent=2))
    else:
        print(f"\n❌ Failed to submit health data: {result['error']}")
        return
    
    print("\n2. RETRIEVING HEALTH DATA")
    print("-" * 30)
    
    # Get recent health data
    result = client.get_health_data(limit=5)
    
    if result["success"]:
        print("✅ Retrieved health data:")
        for entry in result["data"]:
            print(f"  ID: {entry['id']}, Date: {entry['measurement_time']}")
            print(f"  BP: {entry['systolic_bp']}/{entry['diastolic_bp']} mmHg")
            print(f"  Sleep: {entry['sleep_hours']} hours")
            print(f"  Weight: {entry['weight']} kg")
            print("-" * 20)
    else:
        print(f"❌ Failed to retrieve health data: {result['error']}")
    
    print("\n3. HEALTH DATA SUMMARY")
    print("-" * 30)
    
    # Get health summary
    result = client.get_health_summary()
    
    if result["success"]:
        summary = result["data"]
        print("✅ Health Data Summary:")
        print(f"  Total Entries: {summary.get('total_entries', 0)}")
        
        averages = summary.get('averages', {})
        if averages:
            print("  Average Values:")
            for key, value in averages.items():
                if value is not None:
                    print(f"    {key.replace('_', ' ').title()}: {value}")
        
        latest = summary.get('latest_readings', {})
        if latest:
            print("  Latest Readings:")
            for key, value in latest.items():
                if value is not None and key != 'measurement_time':
                    print(f"    {key.replace('_', ' ').title()}: {value}")
    else:
        print(f"❌ Failed to get health summary: {result['error']}")
    
    print("\n4. CHART DATA FOR VISUALIZATION")
    print("-" * 30)
    
    # Get chart data
    result = client.get_chart_data(days=7)
    
    if result["success"]:
        chart_data = result["data"]
        print("✅ Chart Data Retrieved:")
        print(f"  Dates: {len(chart_data.get('dates', []))} entries")
        print(f"  Blood Pressure: {len([x for x in chart_data.get('blood_pressure_systolic', []) if x is not None])} readings")
        print(f"  Weight: {len([x for x in chart_data.get('weight', []) if x is not None])} measurements")
        print(f"  Sleep: {len([x for x in chart_data.get('sleep_hours', []) if x is not None])} records")
        
        # Show sample data points
        if chart_data.get('dates'):
            print("\n  Sample data points:")
            dates = chart_data['dates']
            for i, date_str in enumerate(dates[:3]):  # Show first 3 entries
                print(f"    {date_str}:")
                if chart_data.get('blood_pressure_systolic', [None])[i]:
                    bp_sys = chart_data['blood_pressure_systolic'][i]
                    bp_dia = chart_data['blood_pressure_diastolic'][i]
                    print(f"      Blood Pressure: {bp_sys}/{bp_dia} mmHg")
                if chart_data.get('weight', [None])[i]:
                    print(f"      Weight: {chart_data['weight'][i]} kg")
                if chart_data.get('sleep_hours', [None])[i]:
                    print(f"      Sleep: {chart_data['sleep_hours'][i]} hours")
    else:
        print(f"❌ Failed to get chart data: {result['error']}")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)

def create_sample_entries():
    """Create multiple sample health data entries for testing"""
    print("\nCreating multiple sample entries for better visualization...")
    
    client = HealthDataAPIClient()
    
    # Create sample data for the past week
    import random
    from datetime import timedelta
    
    base_date = datetime.now()
    
    for i in range(7):
        # Create varied sample data
        sample_data = {
            "systolic_bp": round(random.uniform(110, 130), 1),
            "diastolic_bp": round(random.uniform(70, 85), 1),
            "blood_sugar": round(random.uniform(85, 105), 1),
            "sugar_test_type": random.choice(["fasting", "after_meal"]),
            "sleep_hours": round(random.uniform(6.5, 8.5), 1),
            "sleep_quality": random.randint(6, 9),
            "stress_level": random.randint(2, 6),
            "steps_count": random.randint(6000, 12000),
            "exercise_minutes": round(random.uniform(20, 60), 0),
            "weight": round(random.uniform(74, 76), 1),
            "heart_rate": random.randint(65, 80),
            "water_intake": round(random.uniform(1.5, 3.0), 1),
            "mood_score": random.randint(6, 9),
            "energy_level": random.randint(5, 9),
            "measurement_time": (base_date - timedelta(days=i)).isoformat()
        }
        
        result = client.submit_health_data(sample_data)
        if result["success"]:
            print(f"✅ Created entry for {sample_data['measurement_time'][:10]}")
        else:
            print(f"❌ Failed to create entry: {result['error']}")

if __name__ == "__main__":
    print("Health Data API Demo")
    print("Make sure your backend is running on http://localhost:8000")
    
    try:
        # Test API connection
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            
            # Run the main demonstration
            demo_health_data_submission()
            
            # Ask if user wants to create sample data
            create_samples = input("\nWould you like to create sample entries for testing? (y/n): ")
            if create_samples.lower() == 'y':
                create_sample_entries()
            
        else:
            print(f"❌ Backend responded with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Please start the backend first:")
        print("cd backend_api && python main_enhanced.py")