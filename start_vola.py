#!/usr/bin/env python3
"""
VOLA Engine Startup Script
Starts both the FastAPI backend and provides instructions for the frontend, patchged dir


"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("Installing VOLA Engine dependencies...")
    
    # Install backend dependencies
    api_dir = Path("api")
    if api_dir.exists():
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "api/requirements.txt"])
        print("Backend dependencies installed")
    
    # Install frontend dependencies
    app_dir = Path("app")
    if app_dir.exists():
        subprocess.run(["npm", "install"], cwd="app")
        print("Frontend dependencies installed")

def start_backend():
    """Start the FastAPI backend server"""
    print("Starting VOLA Engine Backend...")
    print("Backend will be available at: http://127.0.0.1:8000")
    print("API Documentation: http://127.0.0.1:8000/docs")
    
    api_dir = Path("api")
    if api_dir.exists():
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ], cwd="api")
    else:
        print("API directory not found")

def main():
    print("VOLA Engine - Volatility Linguistics Arbitrage")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("api").exists() or not Path("app").exists():
        print("Please run this script from the vola-engine directory")
        return
    
    # Install dependencies
    install_dependencies()
    
    print("\nVOLA Engine is ready!")
    print("\nTo start the application:")
    print("1. Backend (this script): python start_vola.py")
    print("2. Frontend (new terminal): cd app && npm run dev")
    print("\nAccess points:")
    print("   • Frontend: http://localhost:3000")
    print("   • Backend API: http://127.0.0.1:8000")
    print("   • API Docs: http://127.0.0.1:8000/docs")
    
    print("\nStarting backend server...")
    start_backend()

if __name__ == "__main__":
    main() 
