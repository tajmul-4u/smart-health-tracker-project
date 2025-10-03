#!/bin/bash

# Profile Management Showcase Launcher
# Comprehensive demo of modern professional profile management

echo "🏥 Starting Profile Management Showcase..."
echo "This demonstrates the modern professional design and user-friendly profile management."
echo

# Check if backend is running
echo "🔍 Checking backend API status..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is running - Full functionality available!"
else
    echo "📝 Backend API not detected - Profile form will work in demo mode."
    echo "💡 To enable API saving: cd backend_api && python main_enhanced.py"
fi

echo
echo "🎯 Profile Management Showcase Features:"
echo "• Modern professional design with gradients and animations"
echo "• Comprehensive profile form with 4 organized tabs"
echo "• User-friendly interface with intuitive navigation"
echo "• Real-time validation and error handling"
echo "• API integration for data persistence"
echo "• Responsive design principles"
echo
echo "🚀 Launching Profile Management Showcase..."
echo

# Launch the comprehensive showcase
/home/tajmul/Projects/Python/health-recomand/smart_health_tracker/venv/bin/python profile_management_showcase.py

echo
echo "👋 Profile Management Showcase closed."
echo
echo "🎯 To use in main application:"
echo "./run_smart_health_tracker.sh"
echo "Then click profile icon → '👤 Edit Profile'"