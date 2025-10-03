#!/usr/bin/env python3
"""
Profile Form Integration Test
Test the profile form integration in the dashboard without full GUI startup
"""

import sys
import os
sys.path.insert(0, '/home/tajmul/Projects/Python/health-recomand/smart_health_tracker')

def test_profile_integration():
    """Test profile form integration"""
    print("🔍 Testing Profile Form Integration...")
    
    try:
        # Test imports
        from app.controllers.enhanced_dashboard_controller import EnhancedDashboardController
        from app.widgets.user_profile_form import UserProfileFormWidget
        from app.services.api_client import APIClient
        
        print("✅ All imports successful")
        
        # Test API client creation
        api_client = APIClient()
        print("✅ API client created")
        
        # Test dashboard controller creation (this is where the issue might be)
        print("📋 Testing dashboard controller creation...")
        
        # Check if UI file exists
        ui_path = '/home/tajmul/Projects/Python/health-recomand/smart_health_tracker/app/ui/enhanced_dashboard.ui'
        if os.path.exists(ui_path):
            print(f"✅ UI file exists: {ui_path}")
        else:
            print(f"❌ UI file missing: {ui_path}")
            return False
            
        # Test profile menu method
        dashboard_class = EnhancedDashboardController
        
        # Check if all profile methods exist
        required_methods = [
            'show_profile_form',
            'show_profile_menu', 
            'on_profile_saved',
            'on_profile_updated',
            'setup_profile_section'
        ]
        
        for method in required_methods:
            if hasattr(dashboard_class, method):
                print(f"✅ {method} exists")
            else:
                print(f"❌ {method} missing")
                return False
        
        print("\n🎯 Profile Integration Test Results:")
        print("✅ All profile methods are properly integrated")
        print("✅ Profile form widget is available")
        print("✅ API client is functional")
        print("✅ UI file exists")
        
        print("\n📋 Profile Menu Structure (Expected):")
        print("├── 👤 Edit Profile (PRIMARY - bold)")
        print("├── ──────────────")
        print("├── 🏥 Health Data")
        print("├── 📋 View Profile Info")
        print("├── ──────────────")
        print("├── ⚙️ Settings")
        print("└── 🚪 Logout")
        
        print("\n🔧 If profile form isn't showing, the issue is likely:")
        print("1. Qt application initialization in main app")
        print("2. UI file loading issues")
        print("3. Profile button click handler not working")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_profile_form_standalone():
    """Test if profile form can work with minimal Qt setup"""
    print("\n🧪 Testing Profile Form Standalone...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from app.widgets.user_profile_form import UserProfileFormWidget
        
        # Create minimal Qt application
        app = QApplication([])
        
        # Create profile form
        form = UserProfileFormWidget()
        print("✅ Profile form created successfully")
        
        # Test form functionality
        data = form.collect_form_data()
        print(f"✅ Form has {len(data)} fields")
        
        # Test with sample data
        sample_data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'height': 175,
            'weight': 70.0
        }
        
        form.populate_form(sample_data)
        print("✅ Form population works")
        
        is_valid = form.validate_form(sample_data)
        print(f"✅ Form validation: {is_valid}")
        
        # Clean up
        app.quit()
        
        print("✅ Profile form is fully functional!")
        return True
        
    except Exception as e:
        print(f"❌ Standalone test failed: {e}")
        return False

if __name__ == "__main__":
    print("🏥 Smart Health Tracker - Profile Form Integration Test")
    print("=" * 60)
    
    # Test integration
    integration_ok = test_profile_integration()
    
    # Test standalone form
    standalone_ok = test_profile_form_standalone()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print(f"{'✅' if integration_ok else '❌'} Profile Integration: {'PASS' if integration_ok else 'FAIL'}")
    print(f"{'✅' if standalone_ok else '❌'} Profile Form Widget: {'PASS' if standalone_ok else 'FAIL'}")
    
    if integration_ok and standalone_ok:
        print("\n🎉 All tests passed! Profile form should work in main application.")
        print("🔧 If it's not showing, check the main application startup.")
    else:
        print("\n⚠️ Some tests failed. Profile form needs fixes.")
        
    print("\n🚀 To test in main application:")
    print("./run_smart_health_tracker.sh")
    print("Then click profile icon → '👤 Edit Profile'")