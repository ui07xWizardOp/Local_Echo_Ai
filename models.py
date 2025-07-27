from database import db
from datetime import datetime
from sqlalchemy import JSON

class UserProfile(db.Model):
    """User profile and preferences"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    preferred_language = db.Column(db.String(10), default='en-IN')
    interests = db.Column(db.Text)  # Comma-separated interests
    travel_style = db.Column(db.String(50), default='explorer')  # explorer, relaxed, adventurous, cultural
    mood_history = db.Column(JSON)  # Store mood analysis history
    location_history = db.Column(JSON)  # Store visited locations
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Conversation(db.Model):
    """Store conversation history"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    session_id = db.Column(db.String(100), nullable=False)
    message_type = db.Column(db.String(20))  # 'user' or 'ai'
    content = db.Column(db.Text)
    language = db.Column(db.String(10))
    sentiment = db.Column(db.String(20))
    mood = db.Column(db.String(20))
    location = db.Column(JSON)  # Store lat, lng, city info
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Itinerary(db.Model):
    """Store generated itineraries"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200))
    city = db.Column(db.String(100))
    duration_days = db.Column(db.Integer)
    activities = db.Column(JSON)  # List of activities with details
    transport_info = db.Column(JSON)  # Transport recommendations
    mood_context = db.Column(db.String(50))  # Mood when generated
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CulturalStory(db.Model):
    """Pre-curated cultural stories and local insights"""
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    story_title = db.Column(db.String(200))
    story_content = db.Column(db.Text)
    story_audio_url = db.Column(db.String(500))  # Pre-generated audio
    category = db.Column(db.String(50))  # historical, cultural, folklore, modern
    language = db.Column(db.String(10), default='en-IN')
    tags = db.Column(db.String(200))  # Comma-separated tags
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
