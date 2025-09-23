#!/bin/bash

# Smart Health Tracker Startup Script

echo "=== Smart Health Tracker ==="
echo "Starting the application..."
echo

# Check if virtual environment exists
if [ ! -d "/home/tajmul/Projects/Python/health-recomand/.venv" ]; then
    echo "Error: Virtual environment not found!"
    exit 1
fi

# Set Python path
export PYTHONPATH="/home/tajmul/Projects/Python/health-recomand/smart_health_tracker"
PYTHON_CMD="/home/tajmul/Projects/Python/health-recomand/.venv/bin/python"

# Start backend in background
echo "1. Starting Backend API Server..."
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker/backend_api
$PYTHON_CMD main_simple.py &
BACKEND_PID=$!
echo "   Backend started with PID: $BACKEND_PID"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"

# Wait a moment for backend to start
sleep 3

# Test if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "   ✓ Backend is running successfully"
else
    echo "   ✗ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo
echo "2. Starting Frontend Application..."
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
$PYTHON_CMD app/main.py &
FRONTEND_PID=$!
echo "   Frontend started with PID: $FRONTEND_PID"

echo
echo "=== Application Started Successfully ==="
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo
echo "To stop the application:"
echo "kill $BACKEND_PID $FRONTEND_PID"
echo
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo
    echo "Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "All services stopped."
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT

# Wait for processes
wait