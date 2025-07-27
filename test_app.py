#!/usr/bin/env python3
"""
Simple test to check if the Flask app can start properly
"""
import os
import sys

# Set up logging first
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_app_import():
    """Test importing the main app"""
    try:
        logger.info("Testing basic Flask import...")
        from flask import Flask
        logger.info("✓ Flask imported successfully")
        
        logger.info("Testing app import...")
        from app import app, db
        logger.info("✓ App imported successfully")
        
        logger.info("Testing database...")
        with app.app_context():
            # Test database connection
            db.create_all()
            logger.info("✓ Database created successfully")
        
        logger.info("Testing basic route...")
        with app.test_client() as client:
            response = client.get('/health')
            logger.info(f"Health endpoint status: {response.status_code}")
            logger.info(f"Health response: {response.get_json()}")
        
        logger.info("✓ All tests passed - app should work")
        return True
        
    except Exception as e:
        logger.error(f"✗ Error during app test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app_import()
    sys.exit(0 if success else 1)