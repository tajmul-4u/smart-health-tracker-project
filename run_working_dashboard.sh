#!/bin/bash

# Smart Health Tracker - Working Dashboard Launcher
# This script runs the complete working dashboard

echo "🏥 Smart Health Tracker - Working Dashboard"
echo "=========================================="
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Check for virtual environment
if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Using system Python."
fi

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running"
else
    echo "⚠️  Backend is not running. Starting backend..."
    
    # Start backend in background
    if [ -f "backend_api/main_simple.py" ]; then
        python -m uvicorn backend_api.main_simple:app --reload --port 8000 > backend.log 2>&1 &
        BACKEND_PID=$!
        echo "✅ Backend started (PID: $BACKEND_PID)"
        sleep 3
    else
        echo "⚠️  Backend file not found. Dashboard will run in demo mode."
    fi
fi

# Run the working dashboard
echo ""
echo "🚀 Launching Working Dashboard..."
echo ""

python -m app.controllers.working_dashboard_controller

echo ""
echo "✅ Dashboard closed."
