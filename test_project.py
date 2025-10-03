#!/usr/bin/env python3
"""
Test script to verify GUI components can be imported and basic functionality
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/home/tajmul/Projects/Python/health-recomand/smart_health_tracker')

def test_gui_imports():
    """Test if GUI components can be imported successfully"""
    try:
        print("Testing PyQt5 import...")
        from PyQt5.QtWidgets import QApplication, QWidget
        print("✅ PyQt5 imported successfully")
        
        print("Testing health data input form import...")
        from gui.health_data_input_form import HealthDataInputForm
        print("✅ Health data input form imported successfully")
        
        print("Testing health data charts import...")
        from gui.health_data_charts import HealthDataCharts
        print("✅ Health data charts imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_api_client():
    """Test API client functionality"""
    try:
        import requests
        
        # Test backend health
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is responding")
            return True
        else:
            print(f"❌ Backend API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False

def test_database_connectivity():
    """Test database tables exist and are accessible"""
    try:
        import sqlite3
        
        db_path = "/home/tajmul/Projects/Python/health-recomand/smart_health_tracker/backend_api/smart_health_tracker.db"
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check if all required tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['users', 'habits', 'health_data']
            
            for table in required_tables:
                if table in tables:
                    print(f"✅ Table '{table}' exists")
                    
                    # Check table structure
                    cursor.execute(f"PRAGMA table_info({table});")
                    columns = cursor.fetchall()
                    print(f"   Columns: {len(columns)} columns found")
                else:
                    print(f"❌ Table '{table}' missing")
                    return False
            
            return True
    except Exception as e:
        print(f"❌ Database connectivity error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Running Smart Health Tracker Project Tests")
    print("=" * 50)
    
    tests = [
        ("GUI Components Import", test_gui_imports),
        ("API Connectivity", test_api_client),
        ("Database Connectivity", test_database_connectivity),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! The project is fully functional.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)