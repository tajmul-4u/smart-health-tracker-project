#!/bin/bash

# Profile Form Demo Launcher
# Test the new profile form functionality

echo "👤 Starting Profile Form Demo for Smart Health Tracker..."
echo "This demonstrates the new profile management functionality."
echo

# Check if backend is running
echo "🔍 Checking backend API status..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is running on port 8000"
else
    echo "⚠️  Backend API not detected. Profile form will work offline."
    echo "📝 Note: To enable API saving, start the backend with:"
    echo "   cd backend_api && python main_enhanced.py"
    echo
fi

echo
echo "🎯 Profile Form Demo Features:"
echo "• Comprehensive user profile management"
echo "• Tabbed interface: Personal Info, Contact, Health Profile, Preferences"
echo "• Form validation and error handling"
echo "• API integration for data persistence"
echo "• New profile menu structure (Edit Profile prioritized)"
echo
echo "🚀 Launching Profile Form Demo..."
echo

# Launch the profile form demo
/home/tajmul/Projects/Python/health-recomand/smart_health_tracker/venv/bin/python profile_form_demo.py

echo
echo "👋 Profile Form Demo closed."
echo "The profile functionality is now integrated into the main Smart Health Tracker!"