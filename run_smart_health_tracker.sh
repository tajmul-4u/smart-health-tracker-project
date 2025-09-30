#!/bin/bash

echo "🚀 Starting Smart Health Tracker with Enhanced Dashboard..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the project directory
PROJECT_DIR="/home/tajmul/Projects/Python/health-recomand/smart_health_tracker"
VENV_PYTHON="/home/tajmul/Projects/Python/health-recomand/.venv/bin/python"

echo -e "${BLUE}Starting Backend API Server...${NC}"
cd "$PROJECT_DIR/backend_api"
$VENV_PYTHON main_simple.py &
BACKEND_PID=$!

echo -e "${GREEN}Backend started with PID: $BACKEND_PID${NC}"
echo -e "${YELLOW}Backend API available at: http://localhost:8000${NC}"
echo -e "${YELLOW}API Documentation: http://localhost:8000/docs${NC}"
echo ""

# Wait a moment for backend to start
sleep 3

echo -e "${BLUE}Starting Frontend Application...${NC}"
cd "$PROJECT_DIR/app"
$VENV_PYTHON main.py &
FRONTEND_PID=$!

echo -e "${GREEN}Frontend started with PID: $FRONTEND_PID${NC}"
echo ""

echo -e "${GREEN}✅ Smart Health Tracker is now running!${NC}"
echo ""
echo -e "${YELLOW}Features available:${NC}"
echo "📊 Dashboard Overview with Health Stats"
echo "💪 Habits Management (Sleep, Exercise, Meal Logs)"
echo "❤️ Health Conditions (BP, Sugar, Stress)"
echo "📈 Analytics and Health Trends"
echo "🤖 AI Health Predictions"
echo "👥 Community Insights"
echo "⚙️ Settings"
echo "🔔 Notifications"
echo "👤 Profile Management"
echo ""
echo -e "${YELLOW}To stop the application, press Ctrl+C${NC}"

# Wait for user interrupt
trap "echo ''; echo 'Stopping Smart Health Tracker...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait