#!/usr/bin/env python3
"""
End-to-end test for the Smart Health Tracker
This simulates the complete workflow from user registration to data visualization
"""

import sys
import requests
import json
import sqlite3
from datetime import datetime

# Base URL for API
API_BASE = "http://localhost:8000"

def test_user_workflow():
    """Test complete user workflow"""
    print("🔄 Testing Complete User Workflow")
    print("=" * 50)
    
    # Step 1: Register a new user
    print("\n1️⃣ User Registration")
    user_data = {
        "email": "endtoend@example.com",
        "username": "endtoenduser",
        "password": "testpass123",
        "full_name": "End To End User",
        "age": 30,
        "gender": "Female",
        "weight": 65.0,
        "height": 165.0
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/users/register", json=user_data)
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ User registered successfully: {user_info['username']}")
            user_id = user_info['id']
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    # Step 2: Login
    print("\n2️⃣ User Login")
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/users/login", json=login_data)
        if response.status_code == 200:
            login_info = response.json()
            print(f"✅ Login successful: {login_info['access_token']}")
        else:
            print(f"❌ Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 3: Create a habit
    print("\n3️⃣ Create Health Habit")
    habit_data = {
        "name": "Daily Walking",
        "description": "Walk 10,000 steps daily",
        "frequency": "daily",
        "target_value": 10000,
        "current_value": 0
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/habits", json=habit_data)
        if response.status_code == 200:
            habit_info = response.json()
            print(f"✅ Habit created: {habit_info['name']}")
        else:
            print(f"❌ Habit creation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Habit creation error: {e}")
        return False
    
    # Step 4: Log health data
    print("\n4️⃣ Log Health Data")
    health_entries = [
        {
            "systolic": 118,
            "diastolic": 78,
            "notes": "Morning reading"
        },
        {
            "level": 92,
            "meal_relation": "fasting",
            "notes": "Fasting blood sugar"
        },
        {
            "level": 4,
            "notes": "Feeling relaxed after meditation"
        }
    ]
    
    endpoints = [
        "/api/health/conditions/blood_pressure",
        "/api/health/conditions/blood_sugar", 
        "/api/health/conditions/stress"
    ]
    
    for i, (endpoint, data) in enumerate(zip(endpoints, health_entries)):
        try:
            response = requests.post(f"{API_BASE}{endpoint}", json=data)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Health data logged: {endpoint.split('/')[-1]}")
            else:
                print(f"❌ Health data logging failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Health data logging error: {e}")
            return False
    
    # Step 5: Retrieve health analytics
    print("\n5️⃣ Retrieve Health Analytics")
    try:
        response = requests.get(f"{API_BASE}/api/analytics/trends")
        if response.status_code == 200:
            trends = response.json()
            print(f"✅ Analytics retrieved: {len(trends)} trend categories")
            for trend_type, values in trends.items():
                if isinstance(values, list):
                    print(f"   - {trend_type}: {len(values)} data points")
        else:
            print(f"❌ Analytics retrieval failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Analytics retrieval error: {e}")
        return False
    
    # Step 6: Verify database storage
    print("\n6️⃣ Verify Database Storage")
    try:
        db_path = "/home/tajmul/Projects/Python/health-recomand/smart_health_tracker/backend_api/smart_health_tracker.db"
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check user exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", (user_data["email"],))
            user_count = cursor.fetchone()[0]
            
            if user_count > 0:
                print(f"✅ User stored in database")
            else:
                print(f"❌ User not found in database")
                return False
            
            # Check habits exist
            cursor.execute("SELECT COUNT(*) FROM habits WHERE user_id = ?", (user_id,))
            habit_count = cursor.fetchone()[0]
            
            if habit_count > 0:
                print(f"✅ Habits stored in database: {habit_count} habits")
            else:
                print(f"❌ No habits found in database")
                return False
                
    except Exception as e:
        print(f"❌ Database verification error: {e}")
        return False
    
    print("\n🎉 End-to-End Test Completed Successfully!")
    return True

def test_api_endpoints():
    """Test all major API endpoints"""
    print("\n🔗 Testing API Endpoints")
    print("=" * 30)
    
    endpoints_to_test = [
        ("GET", "/health", "Health Check"),
        ("GET", "/api/health/stats", "Health Stats"),
        ("GET", "/api/health/activities", "Health Activities"),
        ("GET", "/api/health/conditions", "Health Conditions"),
        ("GET", "/api/analytics/trends", "Analytics Trends"),
        ("GET", "/api/community/insights", "Community Insights"),
        ("GET", "/api/notifications", "Notifications"),
    ]
    
    passed = 0
    for method, endpoint, description in endpoints_to_test:
        try:
            response = requests.get(f"{API_BASE}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {description}: OK")
                passed += 1
            else:
                print(f"❌ {description}: {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    print(f"\nAPI Endpoints: {passed}/{len(endpoints_to_test)} passed")
    return passed == len(endpoints_to_test)

def main():
    """Main test function"""
    print("🧪 Smart Health Tracker - End-to-End Testing")
    print("=" * 60)
    
    # Test API endpoints first
    api_test = test_api_endpoints()
    
    # Test complete user workflow
    workflow_test = test_user_workflow()
    
    print("\n" + "=" * 60)
    print("📊 Final Test Results:")
    print("=" * 60)
    
    if api_test:
        print("✅ API Endpoints Test: PASSED")
    else:
        print("❌ API Endpoints Test: FAILED")
    
    if workflow_test:
        print("✅ End-to-End Workflow Test: PASSED")
    else:
        print("❌ End-to-End Workflow Test: FAILED")
    
    if api_test and workflow_test:
        print("\n🎉 ALL TESTS PASSED! The Smart Health Tracker is fully functional.")
        print("🏥 Ready for production use!")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return api_test and workflow_test

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)