# Local Echo AI - Voice-First Travel Companion for India

## Overview

Local Echo AI is a sophisticated voice-based travel assistant specifically designed for the Indian market. The application provides personalized travel recommendations, cultural stories, and local insights through natural language conversations in multiple Indian languages. Users can interact via voice calls (Exotel), WhatsApp messages (Gupshup), or direct web interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Web Interface**: Flask-based web application with Bootstrap UI
- **Templates**: Jinja2 templating with responsive design
- **Static Assets**: CSS styling with custom design system
- **Interactive Elements**: Voice recording, audio playback, and real-time transcription

### Backend Architecture
- **Framework**: Python Flask with SQLAlchemy ORM
- **API Design**: RESTful endpoints with webhook handlers
- **Database**: SQLite (development) with planned PostgreSQL migration
- **Session Management**: Flask sessions with proxy middleware support

### Service-Oriented Architecture
The application follows a service-oriented pattern with distinct modules:
- **Voice Processing**: Speech-to-text and text-to-speech services
- **AI Intelligence**: Gemini integration for conversation and mood analysis
- **Location Services**: Google Maps integration for place discovery
- **Transport Services**: Indian Railways and local transport integration
- **Story Generation**: Cultural content and local insights
- **Mood Tracking**: User sentiment and preference analysis

## Key Components

### Handler Layer
- **Voice Handler**: Main orchestrator for voice interactions
- **Exotel Handler**: Processes incoming voice calls using TwiML
- **Gupshup Handler**: Manages WhatsApp message interactions

### Service Layer
- **Gemini Service**: AI-powered conversation and mood analysis
- **Speech Service**: Google Cloud Speech-to-Text and Text-to-Speech
- **Location Service**: Google Maps integration for place information
- **Transport Service**: Multi-modal transport recommendations
- **Story Service**: Cultural content generation and caching
- **Mood Service**: Advanced mood tracking and pattern analysis

### Data Models
- **UserProfile**: User preferences, language settings, and travel style
- **Conversation**: Complete conversation history with sentiment analysis
- **Itinerary**: Generated travel plans with mood context
- **CulturalStory**: Pre-curated and generated cultural content

### Utility Modules
- **Audio Utils**: Audio format validation and processing
- **Language Utils**: Multi-language detection and translation support

## Data Flow

### Voice Interaction Flow
1. **Input Processing**: Audio received via Exotel, Gupshup, or web interface
2. **Transcription**: Google Cloud Speech-to-Text converts audio to text
3. **Language Detection**: Automatic detection of spoken language
4. **Context Building**: Retrieve user profile and conversation history
5. **Mood Analysis**: Gemini analyzes current mood and travel preferences
6. **Response Generation**: AI generates contextual travel recommendations
7. **Content Enrichment**: Add location data, transport info, and cultural stories
8. **Speech Synthesis**: Convert response to speech in user's preferred language
9. **Response Delivery**: Send via appropriate channel (voice call, WhatsApp, web)

### Data Storage Strategy
- **User Profiles**: Persistent storage of preferences and mood patterns
- **Conversation History**: Complete interaction logs for context building
- **Generated Content**: Caching of itineraries and stories for reuse
- **Cultural Database**: Pre-curated local stories and insights

## External Dependencies

### Google Cloud Platform
- **Speech-to-Text API**: Multi-language voice transcription
- **Text-to-Speech API**: Natural voice synthesis
- **Translation API**: Real-time language translation
- **Maps API**: Location services and place information

### AI Services
- **Google Gemini**: Advanced conversation AI and mood analysis
- **Pydantic Models**: Structured data validation and parsing

### Indian Service Providers
- **Exotel**: Voice calling platform for Indian market
- **Gupshup**: WhatsApp Business API integration
- **Indian Railways API**: Train schedules and booking information

### Frontend Libraries
- **Bootstrap**: Responsive UI framework with dark theme
- **Font Awesome**: Icon library for enhanced UX

## Deployment Strategy

### Environment Configuration
- **Development**: SQLite database with local file storage
- **Production**: PostgreSQL database with cloud storage
- **API Keys**: Environment-based configuration for all external services

### Scaling Considerations
- **Database Migration**: Ready for PostgreSQL upgrade using Drizzle ORM patterns
- **Service Separation**: Microservices-ready architecture
- **Caching Strategy**: Redis integration planned for performance optimization
- **Load Balancing**: Proxy middleware configured for multi-instance deployment

### Indian Market Adaptations
- **Language Support**: 12+ Indian languages with regional dialects
- **Cultural Context**: India-specific travel patterns and preferences
- **Local Integrations**: Indian Railways, local transport, and regional APIs
- **Regulatory Compliance**: Data localization and privacy requirements

### Security and Privacy
- **Data Protection**: User conversation encryption and secure storage
- **API Security**: Rate limiting and authentication for all endpoints
- **Privacy Controls**: User data deletion and export capabilities