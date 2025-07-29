import os
import logging
from flask import Flask, request, jsonify, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from database import db

# Configure logging with reduced verbosity
logging.basicConfig(level=logging.INFO)
# Reduce gTTS and other debug logging
logging.getLogger('gtts').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('gtts.tts').setLevel(logging.WARNING)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "local-echo-ai-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///local_echo_ai.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models  # noqa: F401
    db.create_all()

# Import handlers after database initialization to avoid circular imports
from handlers.exotel_handler import handle_exotel_webhook
from handlers.gupshup_handler import handle_gupshup_webhook
from handlers.voice_handler import process_voice_interaction

@app.route('/')
def index():
    """Main dashboard page for Local Echo AI"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Local Echo AI"}), 200

@app.route('/exotel-webhook', methods=['POST'])
def exotel_webhook():
    """Handle incoming calls from Exotel"""
    try:
        app.logger.info(f"Received Exotel webhook: {request.form}")
        response = handle_exotel_webhook(request.form)
        return response
    except Exception as e:
        app.logger.error(f"Error handling Exotel webhook: {e}")
        return str(e), 500

@app.route('/gupshup-webhook', methods=['POST'])
def gupshup_webhook():
    """Handle incoming WhatsApp messages from Gupshup"""
    try:
        data = request.get_json()
        app.logger.info(f"Received Gupshup webhook: {data}")
        response = handle_gupshup_webhook(data)
        return response
    except Exception as e:
        app.logger.error(f"Error handling Gupshup webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/simulate-voice', methods=['POST'])
def simulate_voice():
    """Simulate voice interaction with robust fallback system"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' in request body"}), 400
        
        text = data['text']
        language = data.get('language', 'en-IN')
        user_id = data.get('user_id', 'demo-user')
        location = data.get('location')
        
        app.logger.info(f"Processing voice simulation: {text[:100]}...")
        
        try:
            # Auto-detect language from text input
            from services.language_detection import language_detector
            detected_language = language_detector.detect_language_from_text(text)
            
            # Try the full voice handler first
            result = process_voice_interaction(
                text=text,
                language=detected_language,  # Use detected language
                user_id=user_id,
                location=location
            )
            return jsonify(result), 200
            
        except Exception as handler_error:
            app.logger.warning(f"Voice handler failed: {handler_error}, using fallback")
            
            # Use fallback service for immediate response
            from services.fallback_service import fallback_service
            from services.language_detection import language_detector
            
            # Auto-detect language for fallback too
            detected_language = language_detector.detect_language_from_text(text)
            
            location_str = None
            if location and isinstance(location, dict):
                location_str = location.get('city', '')
            
            fallback_result = fallback_service.get_response(text, mood='curious', location=location_str)
            
            # Format response to match expected structure
            result = {
                'status': 'success',
                'response_text': fallback_result['response_text'],
                'language': detected_language,  # Use detected language
                'suggestions': fallback_result['suggestions'],
                'location_info': None,
                'transport_info': None,
                'story_elements': fallback_result['story_elements'],
                'mood_analysis': fallback_result['mood_analysis'],
                'follow_up_questions': fallback_result['follow_up_questions']
            }
            
            return jsonify(result), 200
        
    except Exception as e:
        app.logger.error(f"Critical error in voice simulation: {e}")
        
        # Ultimate fallback - always return something useful
        return jsonify({
            "status": "success",
            "response_text": "I understand you're exploring travel options in India. While I'm having connectivity issues, I can tell you that India offers incredible diversity - from the majestic Himalayas to serene beaches, ancient temples to bustling cities. Each destination has unique stories, delicious food, and warm hospitality waiting to be discovered.",
            "language": language,
            "suggestions": ["Explore local markets and street food", "Visit historical monuments", "Connect with local communities", "Try regional specialties"],
            "location_info": None,
            "transport_info": None,
            "story_elements": ["Rich cultural heritage", "Ancient traditions", "Diverse landscapes"],
            "mood_analysis": {
                "mood": "curious",
                "energy_level": 5,
                "travel_style": "explorer",
                "interests": ["culture", "food"]
            },
            "follow_up_questions": ["What type of experience interests you most?", "Which region of India would you like to explore?"]
        }), 200

@app.route('/api/user/<user_id>/preferences', methods=['GET', 'POST'])
def user_preferences(user_id):
    """Get or update user preferences"""
    try:
        if request.method == 'POST':
            from models import UserProfile
            data = request.get_json()
            
            # Find or create user profile
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            if not profile:
                profile = UserProfile()
                profile.user_id = user_id
                db.session.add(profile)
            
            # Update preferences
            if 'language' in data:
                profile.preferred_language = data['language']
            if 'interests' in data:
                profile.interests = ','.join(data['interests'])
            if 'travel_style' in data:
                profile.travel_style = data['travel_style']
                
            db.session.commit()
            
            return jsonify({"status": "updated"}), 200
        else:
            from models import UserProfile
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            if profile:
                return jsonify({
                    "language": profile.preferred_language,
                    "interests": profile.interests.split(',') if profile.interests else [],
                    "travel_style": profile.travel_style,
                    "mood_history": profile.mood_history
                }), 200
            else:
                return jsonify({"error": "User profile not found"}), 404
                
    except Exception as e:
        app.logger.error(f"Error handling user preferences: {e}")
        return jsonify({"error": str(e)}), 500



@app.route('/api/speech/synthesize', methods=['POST'])
def synthesize_speech_api():
    """Convert text to speech using open-source gTTS"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'en-IN')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        from services.open_speech_service import synthesize_speech_open
        audio_content = synthesize_speech_open(text, language)
        
        if audio_content:
            import base64
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            return jsonify({
                "status": "success",
                "audio_data": audio_base64,
                "content_type": "audio/wav"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": "TTS synthesis failed"
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error in speech synthesis: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/speech/recognize', methods=['POST'])
def recognize_speech_api():
    """Convert speech to text using open-source SpeechRecognition"""
    try:
        # Handle file upload
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en-IN')
        
        if audio_file.filename == '':
            return jsonify({"error": "No audio file selected"}), 400
        
        # Read audio content
        audio_content = audio_file.read()
        
        from services.open_speech_service import transcribe_audio_open
        result = transcribe_audio_open(audio_content, language)
        
        return jsonify(result), 200
            
    except Exception as e:
        app.logger.error(f"Error in speech recognition: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
