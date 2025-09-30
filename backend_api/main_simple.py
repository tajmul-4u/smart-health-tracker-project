import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import uvicorn

# Add project paths
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

app = FastAPI(
    title="Smart Health Tracker API",
    description="Backend API for Smart Health Tracker application",
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

# In-memory storage for testing (replace with proper database later)
users_db = []
user_counter = 1

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Health Tracker API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/users/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    global user_counter
    
    # Check if user exists
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user (in production, hash the password!)
    new_user = {
        "id": user_counter,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "age": user.age,
        "gender": user.gender,
        "weight": user.weight,
        "height": user.height,
        "is_active": True,
        "password": user.password  # In production, hash this!
    }
    
    users_db.append(new_user)
    user_counter += 1
    
    return UserResponse(**new_user)

@app.post("/api/users/login")
async def login(user_credentials: UserLogin):
    for user in users_db:
        if user["email"] == user_credentials.email and user["password"] == user_credentials.password:
            # In production, return a proper JWT token
            return {"access_token": "fake_token_for_testing", "token_type": "bearer", "user_id": user["id"]}
    
    raise HTTPException(status_code=401, detail="Incorrect email or password")

@app.get("/api/users/me", response_model=UserResponse)
async def get_current_user():
    # For testing, return the first user if any exist
    if users_db:
        return UserResponse(**users_db[0])
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/api/users/me", response_model=UserResponse)
async def update_current_user(user_update: UserUpdate):
    # For testing, update the first user if any exist
    if not users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[0]  # In production, get user from JWT token
    
    # Update only the fields that are provided
    if user_update.username is not None:
        user["username"] = user_update.username
    if user_update.full_name is not None:
        user["full_name"] = user_update.full_name
    if user_update.age is not None:
        user["age"] = user_update.age
    if user_update.gender is not None:
        user["gender"] = user_update.gender
    if user_update.weight is not None:
        user["weight"] = user_update.weight
    if user_update.height is not None:
        user["height"] = user_update.height
    
    return UserResponse(**user)

# Health tracking endpoints
@app.get("/api/health/stats")
async def get_health_stats():
    """Get quick health statistics"""
    # Sample data - in real app, calculate from user's data
    return {
        "steps": 8450,
        "sleep_hours": 7.5,
        "water_intake": 2.1,
        "mood_score": 8.2
    }

@app.get("/api/health/activities")
async def get_recent_activities():
    """Get recent health activities"""
    # Sample data - in real app, fetch from database
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
    # Sample notifications
    return [
        {"type": "health_alert", "message": "Time for your evening medication", "time": "5 mins ago", "read": False},
        {"type": "achievement", "message": "You've reached your daily step goal!", "time": "2 hours ago", "read": False},
        {"type": "reminder", "message": "Don't forget to log your blood pressure", "time": "1 day ago", "read": True}
    ]

@app.post("/api/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: int):
    """Mark a notification as read"""
    return {"status": "success", "message": "Notification marked as read"}

# Health conditions endpoints
@app.get("/api/health/conditions")
async def get_health_conditions():
    """Get health conditions data"""
    return {
        "blood_pressure": [
            {"date": "2025-09-30", "systolic": 120, "diastolic": 80},
            {"date": "2025-09-29", "systolic": 118, "diastolic": 78},
            {"date": "2025-09-28", "systolic": 122, "diastolic": 82}
        ],
        "blood_sugar": [
            {"date": "2025-09-30", "level": 95, "meal_relation": "fasting"},
            {"date": "2025-09-29", "level": 140, "meal_relation": "after_meal"},
            {"date": "2025-09-28", "level": 88, "meal_relation": "fasting"}
        ],
        "stress_level": [
            {"date": "2025-09-30", "level": 3, "notes": "Feeling relaxed"},
            {"date": "2025-09-29", "level": 7, "notes": "Work deadline stress"},
            {"date": "2025-09-28", "level": 4, "notes": "Normal day"}
        ]
    }

@app.post("/api/health/conditions/blood_pressure")
async def log_blood_pressure(data: dict):
    """Log blood pressure reading"""
    # In real app, save to database
    return {"status": "success", "message": "Blood pressure logged successfully"}

@app.post("/api/health/conditions/blood_sugar")
async def log_blood_sugar(data: dict):
    """Log blood sugar reading"""
    # In real app, save to database
    return {"status": "success", "message": "Blood sugar logged successfully"}

@app.post("/api/health/conditions/stress")
async def log_stress_level(data: dict):
    """Log stress level"""
    # In real app, save to database
    return {"status": "success", "message": "Stress level logged successfully"}

# Analytics endpoints
@app.get("/api/analytics/trends")
async def get_health_trends():
    """Get health trends for analytics"""
    return {
        "weight_trend": [70.2, 70.0, 69.8, 69.9, 70.1],
        "sleep_trend": [7.5, 8.0, 7.2, 6.8, 7.5],
        "steps_trend": [8450, 9200, 7800, 8900, 8450],
        "mood_trend": [8.2, 7.8, 8.5, 7.9, 8.2]
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

if __name__ == "__main__":
    print("Starting Smart Health Tracker Backend API...")
    print("Backend available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    uvicorn.run("main_simple:app", host="0.0.0.0", port=8000, reload=False)