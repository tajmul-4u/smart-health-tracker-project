#!/bin/bash
# Modern Health Input System Launcher
echo "🏥 Starting Modern Health Input System Demo..."

# Set environment
export PYTHONPATH="/home/tajmul/Projects/Python/health-recomand/smart_health_tracker:$PYTHONPATH"

# Check Python environment
echo "🔍 Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found! Please install Python 3."
    exit 1
fi

# Check for virtual environment
VENV_PATH="/home/tajmul/Projects/Python/health-recomand/smart_health_tracker/venv"
if [ -d "$VENV_PATH" ]; then
    echo "✅ Virtual environment found"
    PYTHON_CMD="$VENV_PATH/bin/python"
    PIP_CMD="$VENV_PATH/bin/pip"
else
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
    PYTHON_CMD="$VENV_PATH/bin/python"
    PIP_CMD="$VENV_PATH/bin/pip"
fi

# Check dependencies
echo "📦 Checking dependencies..."
$PYTHON_CMD -c "import PyQt6; print('✅ PyQt6 available')" 2>/dev/null || {
    echo "❌ PyQt6 not found! Installing..."
    $PIP_CMD install PyQt6 PyQt6-Charts
}

$PYTHON_CMD -c "import requests; print('✅ Requests available')" 2>/dev/null || {
    echo "❌ Requests not found! Installing..."
    $PIP_CMD install requests
}

# Check if backend is running
echo "🔍 Checking backend API status..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is running"
    BACKEND_STATUS="connected"
else
    echo "⚠️  Backend API not detected"
    echo "📝 Note: System will work in offline mode"
    echo "💡 To enable full features, start the backend with:"
    echo "   cd backend_api && python main_enhanced.py"
    BACKEND_STATUS="offline"
fi

echo ""
echo "🎯 Modern Health Input System Features:"
echo "────────────────────────────────────────"
echo "⚡ Quick Input Mode      - Fast data entry with smart controls"
echo "📋 Detailed Forms       - Comprehensive health data collection"
echo "🎨 Modern UI Design      - Professional interface with animations"
echo "🤖 Smart Validation     - Real-time input checking and suggestions"
echo "💾 Auto-Save            - Automatic data persistence"
echo "📈 Visual Feedback      - Charts and progress indicators"
echo "🔒 Data Security        - Encrypted storage and transmission"
echo "📱 Responsive Design    - Adapts to different screen sizes"
echo ""

if [ "$BACKEND_STATUS" = "connected" ]; then
    echo "🟢 Status: Full functionality available (Backend connected)"
else
    echo "🟡 Status: Offline mode (Backend not connected)"
fi

echo ""
echo "🚀 Launching Modern Health Input System Demo..."
echo "───────────────────────────────────────────────"

cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker

# Launch the demo
$PYTHON_CMD modern_health_demo.py

echo ""
echo "✅ Modern Health Input System Demo session completed"
echo "Thank you for exploring the enhanced health data management system!"