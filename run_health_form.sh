#!/bin/bash
# Health Data Input Form Launcher

echo "🏥 Starting Health Data Input Form..."
echo "Make sure the backend is running first!"

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running"
else
    echo "❌ Backend not running! Starting backend first..."
    cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker/backend_api
    nohup /home/tajmul/Projects/Python/health-recomand/smart_health_tracker/venv/bin/python main_enhanced.py > backend.log 2>&1 &
    echo "⏳ Waiting for backend to start..."
    sleep 3
fi

# Launch the health data input form
echo "🚀 Launching Health Data Input Form..."
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
/home/tajmul/Projects/Python/health-recomand/smart_health_tracker/venv/bin/python simple_health_form.py

echo "✅ Health Data Input Form closed"