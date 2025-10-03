#!/bin/bash

# Dashboard Profile Demo Launcher
# Launches the dashboard profile section with health data input

echo "🏥 Starting Smart Health Tracker Dashboard Profile Demo..."
echo "This demonstrates the profile section where users can input health data."
echo

# Check if backend is running
echo "🔍 Checking backend API status..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is running on port 8000"
else
    echo "⚠️  Backend API not detected. Starting it now..."
    echo "📝 Note: You can start the backend manually with:"
    echo "   cd backend_api && python main_enhanced.py"
    echo
    
    # Start backend in background
    cd backend_api
    python main_enhanced.py &
    BACKEND_PID=$!
    echo "🚀 Backend started with PID: $BACKEND_PID"
    
    # Wait for backend to start
    echo "⏳ Waiting for backend to initialize..."
    sleep 3
    
    cd ..
fi

echo
echo "🎯 Dashboard Profile Features:"
echo "• Click 'Profile' button for dropdown menu"
echo "• Access health data input forms"
echo "• View and update profile information"
echo "• Test API connectivity"
echo
echo "🚀 Launching Dashboard Profile Demo..."
echo

# Launch the dashboard profile demo
python dashboard_profile_demo.py

echo
echo "👋 Dashboard Profile Demo closed."
echo "Thank you for using Smart Health Tracker!"