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

if __name__ == "__main__":
    print("Starting Smart Health Tracker Backend API...")
    print("Backend available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    uvicorn.run("main_simple:app", host="0.0.0.0", port=8000, reload=False)