#!/usr/bin/env python3
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'backend_api'))

from backend_api.main import app
import uvicorn

if __name__ == "__main__":
    print("Starting Smart Health Tracker Backend API...")
    print("Backend will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)