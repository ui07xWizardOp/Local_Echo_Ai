# Local Echo AI - Voice-First Travel Companion for India

A sophisticated voice-based travel assistant specifically designed for the Indian market. The application provides personalized travel recommendations, cultural stories, and local insights through natural language conversations in multiple Indian languages.

## Features

- **Voice-First Interface**: Natural voice interactions in 12+ Indian languages
- **Mood Detection**: AI-powered sentiment analysis for personalized recommendations  
- **Cultural Stories**: Rich local heritage content and folklore
- **Transport Integration**: Indian Railways and local transport recommendations
- **Multi-Channel Access**: Web interface, phone calls (Exotel), and WhatsApp (Gupshup)
- **Real-time Processing**: Instant speech-to-text and text-to-speech conversion

## Supported Languages

- English (India)
- Hindi (हिंदी)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Bengali (বাংলা)
- Marathi (मराठी)
- And 6+ more Indian languages

## Technology Stack

### Backend
- **Framework**: Python Flask with SQLAlchemy ORM
- **AI Engine**: Google Gemini for conversation and mood analysis
- **Speech Processing**: Open-source gTTS and SpeechRecognition
- **Database**: PostgreSQL (production) / SQLite (development)

### Frontend
- **UI Framework**: Bootstrap with dark theme
- **JavaScript**: Vanilla JS with modern browser APIs
- **Audio Processing**: Web Audio API with MediaRecorder

### External Services
- **Google Cloud**: Maps API for location services
- **Exotel**: Voice calling platform for Indian market
- **Gupshup**: WhatsApp Business API integration

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL (for production)
- FFmpeg (for audio processing)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/local-echo-ai.git
   cd local-echo-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install system dependencies**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install ffmpeg postgresql postgresql-contrib
   
   # macOS
   brew install ffmpeg postgresql
   
   # Windows
   # Download and install FFmpeg from https://ffmpeg.org/download.html
   # Install PostgreSQL from https://www.postgresql.org/download/windows/
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Configure database**
   ```bash
   # Create PostgreSQL database
   createdb local_echo_ai
   
   # Or use SQLite for development (set in .env)
   DATABASE_URL=sqlite:///local_echo.db
   ```

7. **Run the application**
   ```bash
   python main.py
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost/local_echo_ai
# Or for SQLite: DATABASE_URL=sqlite:///local_echo.db

# Session Security
SESSION_SECRET=your-secret-key-here

# AI Services
GEMINI_API_KEY=your-gemini-api-key

# Google Cloud Services (optional)
GOOGLE_MAPS_API_KEY=your-maps-api-key

# Indian Service Providers (for production)
EXOTEL_API_KEY=your-exotel-key
EXOTEL_API_TOKEN=your-exotel-token
GUPSHUP_API_KEY=your-gupshup-key

# Application Settings
FLASK_ENV=development
DEBUG=True
PORT=5000
```

## Manual Deployment

### Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       ffmpeg \
       postgresql-client \
       && rm -rf /var/lib/apt/lists/*
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
   ```

2. **Build and run**
   ```bash
   docker build -t local-echo-ai .
   docker run -p 5000:5000 --env-file .env local-echo-ai
   ```

### AWS Deployment

1. **Install AWS CLI and configure**
   ```bash
   pip install awscli
   aws configure
   ```

2. **Deploy using Elastic Beanstalk**
   ```bash
   pip install awsebcli
   eb init local-echo-ai
   eb create production
   eb deploy
   ```

### Google Cloud Platform

1. **Create app.yaml**
   ```yaml
   runtime: python311
   
   env_variables:
     DATABASE_URL: your-database-url
     GEMINI_API_KEY: your-gemini-key
     SESSION_SECRET: your-session-secret
   
   automatic_scaling:
     min_instances: 1
     max_instances: 10
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

### DigitalOcean App Platform

1. **Create .do/app.yaml**
   ```yaml
   name: local-echo-ai
   services:
   - name: web
     source_dir: /
     github:
       repo: your-username/local-echo-ai
       branch: main
     run_command: gunicorn --bind 0.0.0.0:8080 main:app
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: DATABASE_URL
       scope: RUN_TIME
       value: ${db.DATABASE_URL}
     - key: GEMINI_API_KEY
       scope: RUN_TIME
       value: your-gemini-key
   databases:
   - name: db
     engine: PG
     size: basic-xxs
   ```

### Heroku Deployment

1. **Create Procfile**
   ```
   web: gunicorn main:app
   ```

2. **Deploy**
   ```bash
   heroku create local-echo-ai
   heroku addons:create heroku-postgresql:hobby-dev
   heroku config:set GEMINI_API_KEY=your-key
   git push heroku main
   ```

## API Endpoints

### Voice Interaction
- `POST /simulate-voice` - Process voice interactions
- `POST /api/speech/recognize` - Speech-to-text conversion
- `POST /api/speech/synthesize` - Text-to-speech conversion

### Webhook Handlers
- `POST /exotel-webhook` - Handle Exotel voice calls
- `POST /gupshup-webhook` - Handle WhatsApp messages

### User Management
- `POST /api/user/preferences` - Update user preferences
- `GET /api/user/conversations` - Get conversation history

## Project Structure

```
local-echo-ai/
├── handlers/              # Webhook and interaction handlers
│   ├── voice_handler.py   # Main voice interaction logic
│   ├── exotel_handler.py  # Exotel voice call handler
│   └── gupshup_handler.py # WhatsApp message handler
├── services/              # Business logic services
│   ├── gemini_service.py  # AI conversation service
│   ├── open_speech_service.py # Speech processing
│   ├── location_service.py # Maps and location data
│   ├── transport_service.py # Transport recommendations
│   ├── story_service.py   # Cultural content
│   └── mood_service.py    # Mood analysis
├── utils/                 # Utility modules
│   ├── audio_utils.py     # Audio processing helpers
│   └── language_utils.py  # Language detection
├── templates/             # HTML templates
├── static/                # CSS, JS, assets
├── models.py              # Database models
├── app.py                 # Flask application setup
├── main.py                # Application entry point
├── config.py              # Configuration management
└── requirements.txt       # Python dependencies
```

## Database Schema

### Key Models
- **UserProfile**: User preferences and travel history
- **Conversation**: Complete interaction logs
- **Itinerary**: Generated travel plans
- **CulturalStory**: Curated local content

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Email: support@localecho.ai (if configured)

## Acknowledgments

- Built for the incredible diversity of Indian culture and languages
- Powered by Google Gemini AI
- Designed with accessibility and voice-first principles