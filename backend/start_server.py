#!/usr/bin/env python3
"""
Startup script for the FastAPI backend server.
This ensures the working directory and Python path are set correctly.
"""

import os
import sys
import subprocess

# Get the directory where this script is located (backend directory)
backend_dir = os.path.dirname(os.path.abspath(__file__))

# Change to the backend directory
os.chdir(backend_dir)

# Add the backend directory to Python path
sys.path.insert(0, backend_dir)

# Set environment variables
os.environ['PYTHONPATH'] = backend_dir

# Import and run the app
try:
    import uvicorn
    from app.main import app
    
    print(f"Starting server from directory: {os.getcwd()}")
    print(f"Python path includes: {backend_dir}")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[backend_dir]
    )
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all dependencies are installed")
except Exception as e:
    print(f"Error starting server: {e}")
