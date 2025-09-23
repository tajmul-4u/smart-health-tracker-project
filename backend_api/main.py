import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
try:
    from routes import user_routes, habit_routes
except ImportError:
    # Fallback for different import structures
    from . import routes
    user_routes = routes.user_routes
    habit_routes = routes.habit_routes
import uvicorn

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

# Include routers
app.include_router(user_routes.router, prefix="/api/users", tags=["users"])
app.include_router(habit_routes.router, prefix="/api/habits", tags=["habits"])

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Health Tracker API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
