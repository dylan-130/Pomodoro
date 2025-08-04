#!/usr/bin/env python3
"""
PomodoroFlow - Time Management Application
Quick start script to run both backend and frontend servers
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def run_backend():
    """Start the Flask backend server"""
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    # Initialize database if it doesn't exist
    try:
        subprocess.run([sys.executable, "-c", "from app import init_db; init_db(); print('Database initialized')"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Warning: Could not initialize database")
    
    # Start Flask server
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\nBackend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"Backend server error: {e}")

def run_frontend():
    """Start the React frontend development server"""
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    try:
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\nFrontend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"Frontend server error: {e}")

def main():
    print("🚀 Starting PomodoroFlow...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not (Path(__file__).parent / "backend").exists():
        print("Error: Backend directory not found. Please run this script from the pomodoro-app directory.")
        sys.exit(1)
    
    if not (Path(__file__).parent / "frontend").exists():
        print("Error: Frontend directory not found. Please run this script from the pomodoro-app directory.")
        sys.exit(1)
    
    # Check if npm is available
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: npm is not installed. Please install Node.js and npm first.")
        sys.exit(1)
    
    # Check if frontend dependencies are installed
    frontend_dir = Path(__file__).parent / "frontend"
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        os.chdir(frontend_dir)
        subprocess.run(["npm", "install"], check=True)
    
    # Check if backend dependencies are installed
    backend_dir = Path(__file__).parent / "backend"
    if not (backend_dir / "venv").exists():
        print("🐍 Creating Python virtual environment...")
        os.chdir(backend_dir)
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    print("✅ Dependencies ready!")
    print("\n🌐 Starting servers...")
    print("Backend will run on: http://localhost:5000")
    print("Frontend will run on: http://localhost:5173")
    print("\nPress Ctrl+C to stop both servers")
    print("=" * 50)
    
    # Start both servers in separate threads
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    
    try:
        backend_thread.start()
        time.sleep(2)  # Give backend a moment to start
        frontend_thread.start()
        
        # Wait for both threads
        backend_thread.join()
        frontend_thread.join()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()