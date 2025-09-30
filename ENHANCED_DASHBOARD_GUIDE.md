# Smart Health Tracker - Enhanced Dashboard Guide

## 🚀 Features Overview

Your Smart Health Tracker now includes a comprehensive dashboard with modern navigation and extensive health monitoring capabilities.

## 📋 Navigation Structure

### Left Navigation Menu

**📊 Dashboard**

- Quick health stats overview (Steps, Sleep, Water, Mood)
- Recent activities timeline
- Health alerts and achievements

**💪 Habits**

- Sleep tracking and analysis
- Exercise logging and goals
- Meal logging and nutrition tracking

**❤️ Health Conditions**

- Blood Pressure monitoring
- Blood Sugar level tracking
- Stress level management

**📈 Analytics**

- Health trends and patterns
- Progress charts and graphs
- Comparative analysis over time

**🤖 AI Predictions**

- AI-powered health insights
- Predictive health recommendations
- Risk assessment and alerts

**👥 Community Insights**

- Compare your progress with community averages
- Join health challenges
- Community health rankings

**⚙️ Settings**

- Profile management
- Application preferences
- Data export/import options

### Right Section Features

**🔔 Notifications**

- Health alerts and reminders
- Achievement notifications
- Medication reminders
- Goal completion alerts

**👤 Profile Dropdown**

- User profile information
- Quick access to settings
- Logout functionality

## 🎯 How to Run the Application

### Option 1: Quick Start Script

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
./run_smart_health_tracker.sh
```

### Option 2: Python Launcher (Recommended)

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker
/home/tajmul/Projects/Python/health-recomand/.venv/bin/python start_app.py
```

### Option 3: Manual Start

**Start Backend:**

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker/backend_api
/home/tajmul/Projects/Python/health-recomand/.venv/bin/python main_simple.py
```

**Start Frontend (in new terminal):**

```bash
cd /home/tajmul/Projects/Python/health-recomand/smart_health_tracker/app
/home/tajmul/Projects/Python/health-recomand/.venv/bin/python main.py
```

## 🔧 Technical Implementation

### Backend API Endpoints

**Authentication:**

- `POST /api/users/register` - User registration
- `POST /api/users/login` - User login
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update user profile

**Health Tracking:**

- `GET /api/health/stats` - Quick health statistics
- `GET /api/health/activities` - Recent activities
- `GET /api/health/conditions` - Health conditions data

**Health Conditions:**

- `POST /api/health/conditions/blood_pressure` - Log blood pressure
- `POST /api/health/conditions/blood_sugar` - Log blood sugar
- `POST /api/health/conditions/stress` - Log stress level

**Analytics & Insights:**

- `GET /api/analytics/trends` - Health trends data
- `GET /api/community/insights` - Community comparisons

**Notifications:**

- `GET /api/notifications` - Get notifications
- `POST /api/notifications/{id}/read` - Mark as read

### Frontend Components

**Enhanced Dashboard Controller:**

- Navigation management
- Real-time data updates
- Notification system
- Profile management

**Modern UI Design:**

- Responsive layout
- Dark sidebar navigation
- Colorful stat cards
- Clean, professional styling

## 🎨 Design Features

### Color Scheme

- **Primary Blue:** #3498db (Navigation active, links)
- **Dark Navy:** #2c3e50 (Sidebar, headers)
- **Success Green:** #27ae60 (Positive stats)
- **Warning Orange:** #e67e22 (Attention items)
- **Purple:** #9b59b6 (Mood/wellness)

### Visual Elements

- **Icons:** Emoji-based for better visibility
- **Cards:** Rounded corners with shadows
- **Typography:** Bold headers, readable content
- **Spacing:** Consistent margins and padding

## 🔄 Data Flow

1. **User Login:** Authentication through API
2. **Dashboard Load:** Fetch health stats and activities
3. **Navigation:** Switch between different health modules
4. **Real-time Updates:** Periodic refresh of data
5. **Notifications:** Push health alerts and reminders

## 📱 User Experience

### Dashboard Overview

- At-a-glance health metrics
- Color-coded status indicators
- Recent activity timeline
- Quick action buttons

### Seamless Navigation

- Single-click page switching
- Persistent sidebar
- Breadcrumb navigation
- Smooth transitions

### Interactive Features

- Clickable notifications
- Profile dropdown menu
- Real-time data updates
- Responsive design

## 🔒 Security Features

- Secure user authentication
- Session management
- API token handling
- Profile data protection

## 📊 Data Management

### Health Metrics Tracked

- Daily steps and activity
- Sleep duration and quality
- Water intake monitoring
- Mood and stress levels
- Blood pressure readings
- Blood sugar levels
- Medication compliance

### Analytics Capabilities

- Trend analysis over time
- Goal progress tracking
- Health pattern recognition
- Community comparisons

## 🚨 Notifications System

### Alert Types

- **Health Alerts:** Critical health readings
- **Reminders:** Medication, checkups
- **Achievements:** Goal completions
- **Social:** Community updates

### Notification Management

- Mark as read/unread
- Priority levels
- Custom notification settings
- Push notification support

This enhanced dashboard provides a comprehensive health tracking solution with professional-grade features and modern UI design!

## 🔧 Troubleshooting

### Common Issues and Solutions

**Issue: "ModuleNotFoundError: No module named 'app'"**

- **Solution**: Use Option 2 (Python Launcher) or Option 3 (Manual Start)
- **Reason**: Python import path issues when running from different directories

**Issue: "Port 8000 already in use"**

- **Solution**:
  ```bash
  lsof -ti:8000 | xargs kill -9
  ```
- **Reason**: Previous backend process still running

**Issue: "Backend not responding"**

- **Solution**: Check if backend is running on http://localhost:8000/health
- **Restart backend**: Use Option 3 to manually start backend

**Issue: "Frontend window doesn't appear"**

- **Solution**: Check terminal for Qt/PyQt6 errors
- **Requirements**: Ensure PyQt6 is properly installed

### Quick Verification Commands

**Check Backend Status:**

```bash
curl http://localhost:8000/health
```

**Check API Documentation:**
Open browser: http://localhost:8000/docs

**Check Running Processes:**

```bash
ps aux | grep python
```
