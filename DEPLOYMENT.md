# Manual Deployment Guide for Local Echo AI

This guide helps you deploy Local Echo AI to various platforms without relying on Replit's infrastructure.

## Current Dependencies (from pyproject.toml)

```toml
[project.dependencies]
- email-validator
- flask
- flask-sqlalchemy
- google-cloud-speech
- google-cloud-texttospeech
- google-cloud-translate
- google-genai
- googlemaps
- gtts
- gunicorn
- psycopg2-binary
- pydantic
- pydub
- python-dotenv
- requests
- speechrecognition
- sqlalchemy
- twilio
- werkzeug
```

## Platform-Specific Deployment

### 1. Heroku Deployment

**Setup Steps:**
```bash
# Install Heroku CLI
# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key
heroku config:set SESSION_SECRET=your_secret

# Deploy
git push heroku main
```

**Files needed:**
- ✅ `Procfile` (created)
- ✅ `requirements.txt` (auto-generated from pyproject.toml)

### 2. AWS Elastic Beanstalk

**Setup Steps:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init
eb create production

# Deploy
eb deploy
```

**Configuration:**
- Create `.ebextensions/python.config` for Python settings
- Use RDS for PostgreSQL database
- Set environment variables in EB console

### 3. Google Cloud Platform (App Engine)

**Create `app.yaml`:**
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

**Deploy:**
```bash
gcloud app deploy
```

### 4. DigitalOcean App Platform

**Create `.do/app.yaml`:**
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
databases:
- name: db
  engine: PG
  size: basic-xxs
```

### 5. Docker Deployment (Any Platform)

**Using Docker Compose (recommended for local/VPS):**
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your values

# Run with Docker Compose
docker-compose up -d
```

**Manual Docker:**
```bash
# Build image
docker build -t local-echo-ai .

# Run container
docker run -p 5000:5000 --env-file .env local-echo-ai
```

### 6. VPS/Dedicated Server

**Ubuntu/Debian Setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Install system dependencies
sudo apt install ffmpeg postgresql postgresql-contrib nginx

# Clone repository
git clone https://github.com/yourusername/local-echo-ai.git
cd local-echo-ai

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
sudo -u postgres createdb local_echo_ai
sudo -u postgres createuser -s yourusername

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run application (development)
python run_local.py

# Or use gunicorn (production)
gunicorn --bind 0.0.0.0:5000 main:app
```

**Nginx Configuration (`/etc/nginx/sites-available/local-echo-ai`):**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Environment Configuration

**Required Environment Variables:**
```bash
# Core Configuration
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SESSION_SECRET=your-long-random-secret-key
GEMINI_API_KEY=your-gemini-api-key

# Optional Services
GOOGLE_MAPS_API_KEY=your-maps-key  # For location features
EXOTEL_API_KEY=your-exotel-key     # For phone calls
GUPSHUP_API_KEY=your-gupshup-key   # For WhatsApp

# App Settings
FLASK_ENV=production
DEBUG=False
PORT=5000
HOST=0.0.0.0
```

## Database Setup

### PostgreSQL (Production)
```sql
-- Create database and user
CREATE DATABASE local_echo_ai;
CREATE USER echoai WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE local_echo_ai TO echoai;

-- Connect string
DATABASE_URL=postgresql://echoai:your_password@localhost:5432/local_echo_ai
```

### SQLite (Development)
```bash
# Simple file-based database
DATABASE_URL=sqlite:///local_echo.db
```

## SSL/HTTPS Setup

**Using Certbot (Let's Encrypt):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Monitoring and Logging

**Basic logging setup in production:**
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/local_echo.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

## Performance Optimization

**Gunicorn Configuration:**
```bash
# Create gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 120
max_requests = 1000
max_requests_jitter = 100
```

**Run with config:**
```bash
gunicorn -c gunicorn.conf.py main:app
```

## Removing Replit Dependencies

To make the app platform-independent:

1. **Remove `.replit` file** (optional - only used by Replit)
2. **Use `run_local.py`** instead of Replit workflows
3. **Configure environment variables** in `.env` file
4. **Use standard Python packaging** (pyproject.toml works everywhere)

## Testing Your Deployment

**Health Check Endpoint:**
Add to your Flask app:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

**Test Commands:**
```bash
# Test application
curl http://your-domain.com/health

# Test voice API
curl -X POST http://your-domain.com/api/speech/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "language": "en-IN"}'
```

## Troubleshooting

**Common Issues:**

1. **FFmpeg not found**
   - Install: `sudo apt install ffmpeg` (Linux) or `brew install ffmpeg` (macOS)

2. **Database connection errors**
   - Check DATABASE_URL format
   - Ensure database exists and user has permissions

3. **Import errors**
   - Verify all dependencies installed: `pip install -r requirements.txt`

4. **Audio processing fails**
   - Check FFmpeg installation
   - Verify audio file formats

5. **Gemini API errors**
   - Verify GEMINI_API_KEY is set correctly
   - Check API quotas and billing