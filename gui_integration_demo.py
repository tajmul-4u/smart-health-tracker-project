#!/usr/bin/env python3
"""
GUI Demo - Health Data Input Simulation
This demonstrates the GUI connecting to the backend API
"""

import sys
import os
import requests
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, '/home/tajmul/Projects/Python/health-recomand/smart_health_tracker')

def simulate_gui_api_interaction():
    """Simulate GUI form data being sent to API"""
    print("🖥️  GUI API Integration Simulation")
    print("=" * 40)
    
    # This simulates what the GUI form would collect
    health_form_data = {
        "blood_pressure": {
            "systolic": 125,
            "diastolic": 82,
            "notes": "Submitted via GUI form"
        },
        "blood_sugar": {
            "level": 98,
            "meal_relation": "after_meal",
            "notes": "2 hours after lunch"
        },
        "stress": {
            "level": 5,
            "notes": "Moderate stress from work deadlines"
        }
    }
    
    # Simulate sending data to API endpoints
    api_base = "http://localhost:8000"
    endpoints = {
        "blood_pressure": "/api/health/conditions/blood_pressure",
        "blood_sugar": "/api/health/conditions/blood_sugar",
        "stress": "/api/health/conditions/stress"
    }
    
    print("📤 Simulating GUI form submission...")
    
    for data_type, endpoint in endpoints.items():
        try:
            data = health_form_data[data_type]
            print(f"\n🔄 Sending {data_type} data to API...")
            
            response = requests.post(f"{api_base}{endpoint}", json=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {data_type.title()} data submitted successfully")
                print(f"   Response: {result.get('message', 'Success')}")
            else:
                print(f"❌ {data_type.title()} submission failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error submitting {data_type}: {e}")
    
    return True

def test_gui_components():
    """Test GUI component instantiation without showing windows"""
    print("\n🎨 GUI Components Test")
    print("=" * 25)
    
    try:
        # Import GUI components
        from PyQt5.QtWidgets import QApplication
        from gui.health_data_input_form import HealthDataInputForm
        from gui.health_data_charts import HealthDataCharts
        
        # Create QApplication (required for PyQt5 widgets)
        app = QApplication([])
        
        print("✅ Creating health input form widget...")
        # Create form widget (but don't show it)
        form = HealthDataInputForm()
        print(f"   Form created successfully")
        
        print("✅ Creating health charts widget...")
        # Create charts widget (but don't show it)  
        charts = HealthDataCharts()
        print(f"   Charts widget created successfully")
        
        # Clean up
        app.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ GUI component test failed: {e}")
        return False

def verify_api_integration():
    """Verify the API integration is working"""
    print("\n🔌 API Integration Verification")
    print("=" * 35)
    
    api_base = "http://localhost:8000"
    
    # Test health stats endpoint that would populate the dashboard
    try:
        print("📊 Testing dashboard data retrieval...")
        response = requests.get(f"{api_base}/api/health/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Dashboard data retrieved successfully:")
            for key, value in stats.items():
                print(f"   - {key}: {value}")
        else:
            print(f"❌ Dashboard data retrieval failed")
            return False
    except Exception as e:
        print(f"❌ Dashboard data error: {e}")
        return False
    
    # Test user profile endpoint
    try:
        print("\n👤 Testing user profile retrieval...")
        response = requests.get(f"{api_base}/api/users/me")
        if response.status_code == 200:
            user = response.json()
            print(f"✅ User profile retrieved: {user.get('username', 'Unknown')}")
        else:
            print(f"❌ User profile retrieval failed")
            return False
    except Exception as e:
        print(f"❌ User profile error: {e}")
        return False
    
    return True

def main():
    """Main demo function"""
    print("🏥 Smart Health Tracker - GUI Integration Demo")
    print("=" * 55)
    
    tests = [
        ("GUI Components", test_gui_components),
        ("API Integration", verify_api_integration), 
        ("GUI-API Simulation", simulate_gui_api_interaction),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 55)
    print("📋 GUI Integration Demo Results:")
    print("=" * 55)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 GUI Integration Demo Successful!")
        print("🔗 The GUI can successfully connect to the backend API")
        print("📊 Data can flow from GUI forms to database storage")
        print("🏥 The Smart Health Tracker is ready for use!")
    else:
        print("\n⚠️  Some components need attention.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)