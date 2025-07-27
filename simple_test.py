#!/usr/bin/env python3
"""
Simple direct Flask test without all the complex dependencies
"""
import os
from flask import Flask, jsonify

# Create simple test app
test_app = Flask(__name__)

@test_app.route('/')
def home():
    return "Local Echo AI is running!"

@test_app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "Local Echo AI Test"})

@test_app.route('/api/test')
def api_test():
    return jsonify({
        "status": "success",
        "message": "API is working", 
        "response_text": "Hello! I'm Local Echo AI, your voice-first travel companion for India. I can help you discover amazing places and cultural stories!"
    })

if __name__ == '__main__':
    test_app.run(debug=True, host='0.0.0.0', port=5001)