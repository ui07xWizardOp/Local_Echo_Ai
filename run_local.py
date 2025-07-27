#!/usr/bin/env python3
"""
Local development runner for Local Echo AI
Alternative to using the .replit workflow
"""
import os
import sys
from pathlib import Path

def setup_environment():
    """Setup environment variables from .env file"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    else:
        print("Warning: .env file not found. Using default environment.")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import sqlalchemy
        import speech_recognition
        import gtts
        import pydub
        import google.genai
        print("✓ All Python dependencies found")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Install dependencies with: pip install -r pyproject.toml (or use uv)")
        sys.exit(1)

def check_system_dependencies():
    """Check system dependencies"""
    import subprocess
    
    # Check ffmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✓ FFmpeg found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ FFmpeg not found. Install with:")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/")

def run_application():
    """Run the Flask application"""
    from main import app
    
    # Configuration
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Local Echo AI on http://{host}:{port}")
    print(f"Debug mode: {debug}")
    
    # Run the app
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    print("Local Echo AI - Voice-First Travel Companion")
    print("=" * 50)
    
    # Setup
    setup_environment()
    check_dependencies()
    check_system_dependencies()
    
    print("\nStarting application...")
    run_application()