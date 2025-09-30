#!/usr/bin/env python3

import sys
import os
import subprocess
import time
import signal
from pathlib import Path

# Get project paths
project_root = Path(__file__).parent
venv_python = project_root.parent / ".venv" / "bin" / "python"

def start_backend():
    """Start the backend server"""
    print("🚀 Starting Backend API Server...")
    backend_dir = project_root / "backend_api"
    main_file = backend_dir / "main_simple.py"
    
    os.chdir(backend_dir)
    backend_process = subprocess.Popen([str(venv_python), str(main_file)])
    print(f"✅ Backend started with PID: {backend_process.pid}")
    print("🌐 Backend API available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    return backend_process

def start_frontend():
    """Start the frontend application"""
    print("\n🖥️ Starting Frontend Application...")
    
    # Set up Python path
    os.environ['PYTHONPATH'] = str(project_root)
    
    # Change to project root and run frontend
    os.chdir(project_root)
    main_file = project_root / "app" / "main.py"
    
    frontend_process = subprocess.Popen([str(venv_python), str(main_file)])
    print(f"✅ Frontend started with PID: {frontend_process.pid}")
    return frontend_process

def main():
    """Main startup function"""
    print("🚀 Starting Smart Health Tracker with Enhanced Dashboard...")
    print("=" * 60)
    
    # Start services
    backend_process = start_backend()
    
    # Wait for backend to start
    time.sleep(3)
    
    frontend_process = start_frontend()
    
    print("\n✅ Smart Health Tracker is now running!")
    print("\n🎯 Features available:")
    print("📊 Dashboard Overview with Health Stats")
    print("💪 Habits Management (Sleep, Exercise, Meal Logs)")
    print("❤️ Health Conditions (BP, Sugar, Stress)")
    print("📈 Analytics and Health Trends")
    print("🤖 AI Health Predictions")
    print("👥 Community Insights")
    print("⚙️ Settings")
    print("🔔 Notifications")
    print("👤 Profile Management")
    print("\n⚠️ To stop the application, press Ctrl+C")
    
    def signal_handler(sig, frame):
        print('\n\n🛑 Stopping Smart Health Tracker...')
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Application stopped successfully!")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Wait for processes
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()