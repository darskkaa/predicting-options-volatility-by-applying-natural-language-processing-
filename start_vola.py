#!/usr/bin/env python3
"""
VOLA Engine Startup Script
Professional startup script for the VOLA Engine volatility analysis platform
"""

import subprocess
import sys
import os
from pathlib import Path
import time

def install_dependencies():
    """Install required dependencies with improved error handling"""
    print("Installing VOLA Engine dependencies...")
    
    try:
        # Install backend dependencies
        api_dir = Path("api")
        if api_dir.exists():
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "api/requirements.txt"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Backend dependencies installed successfully")
            else:
                print(f"⚠ Backend installation warnings: {result.stderr}")
        else:
            print("✗ API directory not found")
            return False
        
        # Install frontend dependencies
        app_dir = Path("app")
        if app_dir.exists():
            result = subprocess.run(["npm", "install"], cwd="app", capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Frontend dependencies installed successfully")
            else:
                print(f"⚠ Frontend installation warnings: {result.stderr}")
        else:
            print("✗ App directory not found")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def start_backend():
    """Start the FastAPI backend server with enhanced logging"""
    print("\nStarting VOLA Engine Backend...")
    print("=" * 50)
    print("Backend will be available at: http://127.0.0.1:8000")
    print("API Documentation: http://127.0.0.1:8000/docs")
    print("Health Check: http://127.0.0.1:8000/health")
    print("=" * 50)
    
    api_dir = Path("api")
    if api_dir.exists():
        try:
            subprocess.run([
                sys.executable, "-m", "uvicorn", 
                "main:app", 
                "--host", "127.0.0.1", 
                "--port", "8000", 
                "--reload"
            ], cwd="api")
        except KeyboardInterrupt:
            print("\n✓ Backend server stopped gracefully")
        except Exception as e:
            print(f"✗ Error starting backend: {e}")
    else:
        print("✗ API directory not found")

def main():
    print("VOLA Engine - Volatility Linguistics Arbitrage")
    print("Advanced Quantitative Analysis Platform")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("api").exists() or not Path("app").exists():
        print("✗ Error: Please run this script from the vola-engine directory")
        print("   Expected structure: vola-engine/")
        print("                      ├── api/")
        print("                      └── app/")
        return
    
    print("✓ Directory structure validated")
    
    # Install dependencies
    if not install_dependencies():
        print("✗ Failed to install dependencies. Please check the errors above.")
        return
    
    print("\nVOLA Engine is ready!")
    print("\nTo start the application:")
    print("1. Backend (this script): python start_vola.py")
    print("2. Frontend (new terminal): cd app && npm run dev")
    print("\nAccess points:")
    print("   • Frontend: http://localhost:3000")
    print("   • Backend API: http://127.0.0.1:8000")
    print("   • API Docs: http://127.0.0.1:8000/docs")
    print("   • Health Check: http://127.0.0.1:8000/health")
    
    print("\nStarting backend server...")
    time.sleep(1)  # Brief pause for better UX
    start_backend()

if __name__ == "__main__":
    main() 
