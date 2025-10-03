import sys
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, date
import uvicorn
import hashlib

# Add project paths
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

# Import database and models
from app.database.local_db import get_db, SessionLocal, engine, Base
from app.models.user_model import User as UserORM
from app.models.habit_model import Habit as HabitORM
from app.models.health_data_model import HealthData as HealthDataORM

# Import routes
try:
    from routes.health_data_routes import router as health_data_router
except ImportError:
    health_data_router = None

app = FastAPI(
    title="Smart Health Tracker API - Enhanced",
    description="Backend API for Smart Health Tracker application with database persistence",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Include health data routes
if health_data_router:
    app.include_router(health_data_router, tags=["health-data"])

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str = ""
    age: int = 0
    gender: str = "Other"
    weight: float = 70.0
    height: float = 170.0

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    age: int = 0
    gender: str = "Other"
    weight: float = 70.0
    height: float = 170.0
    is_active: bool = True

    class Config:
        from_attributes = True

class HealthDataCreate(BaseModel):
    data_type: str  # "blood_pressure", "blood_sugar", "stress", "steps", "sleep", "water"
    value: float
    secondary_value: Optional[float] = None  # For blood pressure diastolic
    notes: Optional[str] = None
    recorded_date: Optional[date] = None

class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: str = "daily"
    target_value: int = 1
    current_value: int = 0

class HabitResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    frequency: str
    target_value: int
    current_value: int
    user_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Helper functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

# Create a simple session to store logged-in users (in production, use proper JWT)
current_user_id = None

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Health Tracker API - Enhanced"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

@app.post("/api/users/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(UserORM).filter(UserORM.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = hash_password(user.password)
    new_user = UserORM(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        age=user.age,
        gender=user.gender,
        weight=user.weight,
        height=user.height,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    global current_user_id
    current_user_id = new_user.id
    
    return new_user

@app.post("/api/users/login")
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserORM).filter(UserORM.email == user_credentials.email).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    global current_user_id
    current_user_id = user.id
    
    return {
        "access_token": f"user_token_{user.id}", 
        "token_type": "bearer", 
        "user_id": user.id,
        "message": "Login successful"
    }

@app.get("/api/users/me", response_model=UserResponse)
async def get_current_user(db: Session = Depends(get_db)):
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = db.query(UserORM).filter(UserORM.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@app.put("/api/users/me", response_model=UserResponse)
async def update_current_user(user_update: UserUpdate, db: Session = Depends(get_db)):
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = db.query(UserORM).filter(UserORM.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only the fields that are provided
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return user

# Habit management endpoints
@app.post("/api/habits", response_model=HabitResponse)
async def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    new_habit = HabitORM(
        name=habit.name,
        description=habit.description,
        frequency=habit.frequency,
        target_value=habit.target_value,
        current_value=habit.current_value,
        user_id=current_user_id,
        is_active=True
    )
    
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    
    return new_habit

@app.get("/api/habits", response_model=List[HabitResponse])
async def get_habits(db: Session = Depends(get_db)):
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    habits = db.query(HabitORM).filter(HabitORM.user_id == current_user_id).all()
    return habits

@app.put("/api/habits/{habit_id}/progress")
async def update_habit_progress(habit_id: int, progress: dict, db: Session = Depends(get_db)):
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    habit = db.query(HabitORM).filter(
        HabitORM.id == habit_id, 
        HabitORM.user_id == current_user_id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    habit.current_value = progress.get("current_value", habit.current_value)
    habit.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(habit)
    
    return {"status": "success", "message": "Habit progress updated", "habit": habit}

# Health tracking endpoints
@app.get("/api/health/stats")
async def get_health_stats(db: Session = Depends(get_db)):
    """Get quick health statistics for current user"""
    if not current_user_id:
        # Return sample data for unauthenticated users
        return {
            "steps": 8450,
            "sleep_hours": 7.5,
            "water_intake": 2.1,
            "mood_score": 8.2,
            "user_authenticated": False
        }
    
    # In a real implementation, calculate from user's actual data
    # For now, return sample data with user authentication
    return {
        "steps": 8450,
        "sleep_hours": 7.5,
        "water_intake": 2.1,
        "mood_score": 8.2,
        "user_authenticated": True,
        "user_id": current_user_id
    }

@app.get("/api/health/activities")
async def get_recent_activities():
    """Get recent health activities"""
    # Sample data - in real app, fetch from database based on current user
    return [
        {"activity": "Walked 8,450 steps today", "time": "2 hours ago", "type": "exercise"},
        {"activity": "Slept 7.5 hours last night", "time": "8 hours ago", "type": "sleep"},
        {"activity": "Drank 2.1L water today", "time": "1 hour ago", "type": "hydration"},
        {"activity": "Logged breakfast: Oatmeal with fruits", "time": "3 hours ago", "type": "nutrition"},
        {"activity": "Took morning medication", "time": "4 hours ago", "type": "medication"},
        {"activity": "Completed 10-minute meditation", "time": "1 day ago", "type": "wellness"},
        {"activity": "Blood pressure recorded: 120/80", "time": "2 days ago", "type": "health_condition"}
    ]

@app.get("/api/notifications")
async def get_notifications():
    """Get user notifications"""
    return [
        {"id": 1, "type": "health_alert", "message": "Time for your evening medication", "time": "5 mins ago", "read": False},
        {"id": 2, "type": "achievement", "message": "You've reached your daily step goal!", "time": "2 hours ago", "read": False},
        {"id": 3, "type": "reminder", "message": "Don't forget to log your blood pressure", "time": "1 day ago", "read": True}
    ]

@app.post("/api/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: int):
    """Mark a notification as read"""
    return {"status": "success", "message": "Notification marked as read", "notification_id": notification_id}

# Health conditions endpoints
@app.get("/api/health/conditions")
async def get_health_conditions():
    """Get health conditions data"""
    return {
        "blood_pressure": [
            {"date": "2025-10-03", "systolic": 120, "diastolic": 80},
            {"date": "2025-10-02", "systolic": 118, "diastolic": 78},
            {"date": "2025-10-01", "systolic": 122, "diastolic": 82}
        ],
        "blood_sugar": [
            {"date": "2025-10-03", "level": 95, "meal_relation": "fasting"},
            {"date": "2025-10-02", "level": 140, "meal_relation": "after_meal"},
            {"date": "2025-10-01", "level": 88, "meal_relation": "fasting"}
        ],
        "stress_level": [
            {"date": "2025-10-03", "level": 3, "notes": "Feeling relaxed"},
            {"date": "2025-10-02", "level": 7, "notes": "Work deadline stress"},
            {"date": "2025-10-01", "level": 4, "notes": "Normal day"}
        ]
    }

@app.post("/api/health/conditions/blood_pressure")
async def log_blood_pressure(data: dict, db: Session = Depends(get_db)):
    """Log blood pressure reading"""
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # In a real implementation, save to a health_data table
    # For now, just return success
    return {
        "status": "success", 
        "message": "Blood pressure logged successfully",
        "data": data,
        "user_id": current_user_id,
        "recorded_at": datetime.utcnow().isoformat()
    }

@app.post("/api/health/conditions/blood_sugar")
async def log_blood_sugar(data: dict, db: Session = Depends(get_db)):
    """Log blood sugar reading"""
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return {
        "status": "success", 
        "message": "Blood sugar logged successfully",
        "data": data,
        "user_id": current_user_id,
        "recorded_at": datetime.utcnow().isoformat()
    }

@app.post("/api/health/conditions/stress")
async def log_stress_level(data: dict, db: Session = Depends(get_db)):
    """Log stress level"""
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return {
        "status": "success", 
        "message": "Stress level logged successfully",
        "data": data,
        "user_id": current_user_id,
        "recorded_at": datetime.utcnow().isoformat()
    }

# Analytics endpoints
@app.get("/api/analytics/trends")
async def get_health_trends():
    """Get health trends for analytics"""
    return {
        "weight_trend": [70.2, 70.0, 69.8, 69.9, 70.1],
        "sleep_trend": [7.5, 8.0, 7.2, 6.8, 7.5],
        "steps_trend": [8450, 9200, 7800, 8900, 8450],
        "mood_trend": [8.2, 7.8, 8.5, 7.9, 8.2],
        "user_authenticated": current_user_id is not None
    }

# Community endpoints
@app.get("/api/community/insights")
async def get_community_insights():
    """Get community health insights"""
    return {
        "average_steps": 7500,
        "average_sleep": 7.2,
        "user_ranking": {
            "steps": 85,  # percentile
            "sleep": 78,
            "consistency": 92
        },
        "challenges": [
            {"name": "10K Steps Challenge", "participants": 1250, "user_joined": True},
            {"name": "Sleep Better Challenge", "participants": 890, "user_joined": False},
            {"name": "Mindful Minutes", "participants": 650, "user_joined": True}
        ]
    }

# Debug endpoints
@app.get("/api/debug/users")
async def debug_get_all_users(db: Session = Depends(get_db)):
    """Debug endpoint to see all users in database"""
    users = db.query(UserORM).all()
    return {
        "total_users": len(users),
        "users": [{"id": u.id, "email": u.email, "username": u.username} for u in users],
        "current_user_id": current_user_id
    }

@app.get("/api/debug/habits")
async def debug_get_all_habits(db: Session = Depends(get_db)):
    """Debug endpoint to see all habits in database"""
    habits = db.query(HabitORM).all()
    return {
        "total_habits": len(habits),
        "habits": [{"id": h.id, "name": h.name, "user_id": h.user_id} for h in habits]
    }

if __name__ == "__main__":
    print("🚀 Starting Smart Health Tracker Backend API - Enhanced...")
    print("📊 Backend available at: http://localhost:8000")
    print("📖 API documentation: http://localhost:8000/docs")
    print("💾 Database: SQLite with real persistence")
    print("🔐 Authentication: Simple session-based")
    print("⚡ Features: User registration, habits, health tracking")
    print("🛑 Press Ctrl+C to stop the server")
    uvicorn.run("main_enhanced:app", host="0.0.0.0", port=8000, reload=False)