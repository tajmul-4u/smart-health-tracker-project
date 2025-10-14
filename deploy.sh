#!/bin/bash

# Smart Health Tracker - Production Deployment Script

set -e  # Exit on any error

echo "🚀 Smart Health Tracker - Production Deployment"
echo "=============================================="
echo

# Configuration
PROJECT_DIR="/home/tajmul/Projects/Python/health-recomand/smart_health_tracker"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="$PROJECT_DIR/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Pre-deployment checks
log "🔍 Running pre-deployment checks..."

# Check if running as correct user
if [ "$USER" != "tajmul" ]; then
    warn "Not running as expected user. Current user: $USER"
fi

# Check Python version
if ! python3 --version | grep -q "Python 3\.[8-9]\|Python 3\.1[0-9]"; then
    error "Python 3.8+ required. Current version: $(python3 --version)"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    log "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
log "🔧 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Update pip
log "⬆️  Updating pip..."
pip install --upgrade pip

# Install dependencies
log "📥 Installing dependencies..."
pip install -r requirements.txt

# Create logs directory
mkdir -p "$LOG_DIR"

# Initialize database
log "🗄️  Initializing database..."
python init_db.py

# Check environment configuration
if [ ! -f ".env" ]; then
    if [ -f ".env.template" ]; then
        log "📝 Creating .env from template..."
        cp .env.template .env
        warn "Please edit .env file with your production settings!"
    else
        warn ".env file not found. Using default configuration."
    fi
fi

# Run security checks
log "🔒 Running security checks..."

# Check JWT secret
if grep -q "change-this-to-a-secure-random-string" .env 2>/dev/null; then
    warn "Default JWT secret detected! Please change it in .env file."
fi

# Test API endpoints
log "🧪 Testing API endpoints..."
python3 -c "
import sys
sys.path.append('.')
try:
    from backend_api.main import app
    print('✅ API imports successful')
except Exception as e:
    print(f'❌ API import failed: {e}')
    sys.exit(1)
"

# Test GUI imports
log "🖥️  Testing GUI components..."
python3 -c "
import sys
sys.path.append('.')
try:
    from app.main import SmartHealthTracker
    print('✅ GUI imports successful')
except Exception as e:
    print(f'❌ GUI import failed: {e}')
    sys.exit(1)
"

# Create systemd service (optional)
create_systemd_service() {
    if [ "$EUID" -eq 0 ]; then
        log "📋 Creating systemd service..."
        cat > /etc/systemd/system/smart-health-tracker.service << EOF
[Unit]
Description=Smart Health Tracker Backend
After=network.target

[Service]
Type=simple
User=tajmul
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$VENV_DIR/bin
ExecStart=$VENV_DIR/bin/python backend_api/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
        
        systemctl daemon-reload
        systemctl enable smart-health-tracker.service
        log "✅ Systemd service created and enabled"
    else
        warn "Run as root to create systemd service"
    fi
}

# Performance optimization
log "⚡ Applying performance optimizations..."
export PYTHONOPTIMIZE=1
export PYTHONDONTWRITEBYTECODE=1

# Final deployment summary
echo
echo "🎉 DEPLOYMENT COMPLETE!"
echo "======================"
echo "✅ Virtual environment: $VENV_DIR"
echo "✅ Dependencies installed"
echo "✅ Database initialized"
echo "✅ Security checks completed"
echo "✅ Application tested"
echo
echo "🚀 To start the application:"
echo "   ./start_project.sh"
echo
echo "📊 Monitor logs in: $LOG_DIR"
echo "🔧 Configuration: .env"
echo "📚 API Documentation: http://localhost:8000/docs"
echo

# Ask about systemd service
read -p "Create systemd service for auto-start? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    create_systemd_service
fi

log "🏁 Production deployment completed successfully!"