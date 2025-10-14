# 🚀 Smart Health Tracker - Run Commands

This document provides all the ways to run the Smart Health Tracker project components.

## 📋 Quick Start

### Option 1: Complete Application (Recommended)

```bash
# Run both backend and frontend together (Login → Modern Dashboard)
./start_project.sh
```

### Option 2: Modern Dashboard Only

```bash
# Run the modern working dashboard directly
./run_working_dashboard.sh
```

### Option 3: Manual Setup

```bash
# 1. Start backend
./start_backend.sh

# 2. In another terminal, start frontend
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
source venv/bin/activate
python -m app.controllers.working_dashboard_controller
```

---

## 🔧 Detailed Run Options

### 1. Full Application Stack

#### `start_project.sh` - Complete Setup

Starts both backend API and frontend application.

```bash
./start_project.sh
```

**What it does:**

- Checks for virtual environment
- Starts FastAPI backend on port 8000
- Shows login/registration window
- After successful login, launches modern dashboard
- Provides cleanup on Ctrl+C

**Requirements:**

- Virtual environment at `/home/tajmul/Projects/Python/health-recomand/.venv`
- All dependencies installed

---

### 2. Backend Only

#### `start_backend.sh` - API Server

Starts only the FastAPI backend server.

```bash
./start_backend.sh
```

**Manual Backend Start:**

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker/backend_api
/home/tajmul/Projects/Python/health-recomand/.venv/bin/python main_simple.py
```

**Backend URLs:**

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

### 3. Frontend Applications

#### Working Dashboard (Main Application)

```bash
./run_working_dashboard.sh
```

**Manual Dashboard Start:**

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
source venv/bin/activate
python -m app.controllers.working_dashboard_controller
```

#### Original Application Entry Point

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
source venv/bin/activate
python app/main.py
```

---

## 🔍 Component-Specific Commands

### Backend API Server

#### Using uvicorn directly:

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
source venv/bin/activate
uvicorn backend_api.main_simple:app --reload --port 8000
```

#### Background mode:

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
source venv/bin/activate
nohup python -m uvicorn backend_api.main_simple:app --port 8000 > backend.log 2>&1 &
```

### Frontend Controllers

#### Working Dashboard Controller:

```bash
python -m app.controllers.working_dashboard_controller
```

#### Login Controller:

```bash
python -m app.controllers.login_controller
```

### Widgets and Components

#### Modern Health Input Widget:

```bash
python -m app.widgets.modern_health_input
```

#### User Profile Form:

```bash
python -m app.widgets.user_profile_form
```

---

## 🛠️ Development Commands

### Database Operations

#### Initialize Database:

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
source venv/bin/activate
python init_db.py
```

### Testing

#### Run Tests:

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
source venv/bin/activate
python -m pytest tests/
```

#### Test Specific Components:

```bash
# Test user functionality
python tests/test_user.py

# Test habit functionality
python tests/test_habit.py
```

---

## 📦 Environment Setup

### Virtual Environment

#### Create Virtual Environment (if needed):

```bash
cd /home/tajmul/Projects/Python/health-recomand
python -m venv .venv
source .venv/bin/activate
```

#### Install Dependencies:

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
pip install -r requirements.txt
```

### Alternative Virtual Environment Location

If using local venv:

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔄 Process Management

### Check Running Processes

```bash
# Check for backend
curl http://localhost:8000/health

# Check for dashboard
ps aux | grep working_dashboard

# Check all Python processes
ps aux | grep python | grep -v grep
```

### Stop Processes

```bash
# Stop backend
pkill -f "uvicorn backend_api"

# Stop dashboard
pkill -f "working_dashboard"

# Stop all project processes
pkill -f "smart_health_tracker"
```

### Restart Everything

```bash
# Kill existing processes
pkill -f "uvicorn backend_api"
pkill -f "working_dashboard"

# Wait a moment
sleep 2

# Restart
./start_project.sh
```

---

## 🎯 Recommended Workflows

### For Development:

1. Start backend in one terminal: `./start_backend.sh`
2. Start dashboard in another: `./run_working_dashboard.sh`
3. Use separate terminals for easy debugging

### For Demo/Testing:

1. Use complete setup: `./start_project.sh` (Login → Dashboard)
2. Or run dashboard directly: `./run_working_dashboard.sh`

### For Production:

1. Start backend with nohup (background)
2. Use systemd or supervisor for process management
3. Configure proper logging

---

## 🐛 Troubleshooting

### Common Issues

#### Backend Won't Start:

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process using port 8000
kill -9 $(lsof -t -i :8000)
```

#### Frontend Won't Start:

```bash
# Check PyQt6 installation
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"

# Reinstall if needed
pip install PyQt6 PyQt6-Charts
```

#### Virtual Environment Issues:

```bash
# Check current environment
which python
echo $VIRTUAL_ENV

# Ensure correct activation
source venv/bin/activate
```

#### Database Issues:

```bash
# Reinitialize database
rm smart_health_tracker.db
python init_db.py
```

### Log Files

- Backend logs: `backend.log` (if using nohup)
- Check terminal output for errors
- Use `python -v` for verbose debugging

---

## 📚 Additional Resources

### Configuration Files:

- `requirements.txt` - Python dependencies
- `app/utils/config.py` - Application configuration
- `backend_api/config.py` - Backend configuration

### Documentation Files:

- `README.md` - Project overview
- `ENHANCED_DASHBOARD_GUIDE.md` - Dashboard documentation
- `MODERN_DASHBOARD_UPDATE.md` - Modern UI features
- `WORKING_DASHBOARD_GUIDE.md` - Working dashboard guide

### Quick Reference:

- **Main Application**: `./start_project.sh`
- **Dashboard Only**: `./run_working_dashboard.sh`
- **Backend Only**: `./start_backend.sh`
- **Health Check**: `curl http://localhost:8000/health`

---

## 🎉 Success Indicators

When everything is working correctly, you should see:

✅ **Backend Running:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

✅ **Frontend Running:**

- Dashboard window opens
- Title: "🏥 Smart Health Tracker - Dashboard"
- Left sidebar with navigation
- Modern UI with gradients and cards

✅ **API Response:**

```bash
curl http://localhost:8000/health
# Returns: {"status":"healthy"}
```

---

**Happy health tracking! 🏥💪📊**
