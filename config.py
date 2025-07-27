import os

class Config:
    """Configuration settings for Local Echo AI"""
    
    # API Keys from environment variables
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    MAPS_API_KEY = os.environ.get("MAPS_API_KEY")
    
    # Indian service providers
    EXOTEL_API_KEY = os.environ.get("EXOTEL_API_KEY")
    EXOTEL_API_TOKEN = os.environ.get("EXOTEL_API_TOKEN")
    EXOTEL_SID = os.environ.get("EXOTEL_SID")
    EXOTEL_SUBDOMAIN = os.environ.get("EXOTEL_SUBDOMAIN")
    
    GUPSHUP_API_KEY = os.environ.get("GUPSHUP_API_KEY")
    GUPSHUP_APP_NAME = os.environ.get("GUPSHUP_APP_NAME")
    
    # Indian Railways API
    RAILWAYS_API_KEY = os.environ.get("RAILWAYS_API_KEY")
    
    # Language settings
    SUPPORTED_LANGUAGES = {
        'en-IN': 'English (India)',
        'hi-IN': 'Hindi',
        'ta-IN': 'Tamil',
        'te-IN': 'Telugu',
        'bn-IN': 'Bengali',
        'mr-IN': 'Marathi',
        'gu-IN': 'Gujarati',
        'kn-IN': 'Kannada',
        'ml-IN': 'Malayalam',
        'pa-IN': 'Punjabi',
        'or-IN': 'Odia',
        'as-IN': 'Assamese'
    }
    
    # Voice settings
    DEFAULT_VOICE_LANGUAGE = 'en-IN'
    VOICE_MODELS = {
        'en-IN': 'en-IN-Standard-A',
        'hi-IN': 'hi-IN-Standard-A',
        'ta-IN': 'ta-IN-Standard-A',
        'te-IN': 'te-IN-Standard-A',
        'bn-IN': 'bn-IN-Standard-A',
        'mr-IN': 'mr-IN-Standard-A',
        'gu-IN': 'gu-IN-Standard-A',
        'kn-IN': 'kn-IN-Standard-A',
        'ml-IN': 'ml-IN-Standard-A'
    }
    
    # Indian cities configuration
    MAJOR_INDIAN_CITIES = [
        'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata',
        'Pune', 'Ahmedabad', 'Jaipur', 'Surat', 'Lucknow', 'Kanpur',
        'Nagpur', 'Visakhapatnam', 'Indore', 'Thane', 'Bhopal', 'Pimpri-Chinchwad',
        'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik',
        'Faridabad', 'Meerut', 'Rajkot', 'Kalyan-Dombivali', 'Vasai-Virar',
        'Varanasi', 'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar',
        'Navi Mumbai', 'Allahabad', 'Ranchi', 'Haora', 'Coimbatore',
        'Jabalpur', 'Gwalior', 'Vijayawada', 'Jodhpur', 'Madurai'
    ]
    
    # Transport APIs
    TRANSPORT_APIS = {
        'railways': 'https://indianrailapi.com/api/v2/',
        'delhi_metro': 'http://delhimetrorail.com/api/',
        'mumbai_local': 'https://api.mumbailocal.in/',
        'bmtc': 'https://mybmtc.karnataka.gov.in/api/',
        'chennai_metro': 'https://chennaimetrorail.org/api/'
    }
