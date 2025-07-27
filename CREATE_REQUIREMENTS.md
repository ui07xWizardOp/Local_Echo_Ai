# How to Create requirements.txt

Since this project uses `pyproject.toml` for dependency management, you have several options to create a `requirements.txt` file for deployment:

## Method 1: From Current Environment (Recommended)

If you're in the working environment with all dependencies installed:

```bash
pip freeze > requirements.txt
```

## Method 2: Use the Pre-generated File

I've created `requirements_for_deployment.txt` with all the dependencies from your `pyproject.toml`. You can rename it:

```bash
cp requirements_for_deployment.txt requirements.txt
```

## Method 3: Generate from pyproject.toml

If you have `pip-tools` installed:

```bash
# Install pip-tools
pip install pip-tools

# Generate requirements.txt from pyproject.toml
pip-compile pyproject.toml
```

## Method 4: Extract from pyproject.toml manually

The dependencies in your `pyproject.toml` are:

```
email-validator>=2.2.0
flask>=3.1.1
flask-sqlalchemy>=3.1.1
google-cloud-speech>=2.33.0
google-cloud-texttospeech>=2.27.0
google-cloud-translate>=3.21.1
google-genai>=1.27.0
googlemaps>=4.10.0
gtts>=2.5.4
gunicorn>=23.0.0
psycopg2-binary>=2.9.10
pydantic>=2.11.7
pydub>=0.25.1
python-dotenv>=1.1.1
requests>=2.32.4
speechrecognition>=3.14.3
sqlalchemy>=2.0.41
twilio>=9.7.0
werkzeug>=3.1.3
```

## For Different Platforms:

**Heroku**: Auto-detects dependencies from `pyproject.toml`, no requirements.txt needed
**Docker**: Can use either `pyproject.toml` or `requirements.txt`
**Traditional deployment**: Usually expects `requirements.txt`

## Recommendation:

Use the pre-generated `requirements_for_deployment.txt` file - it contains all your current dependencies with proper version constraints.