"""Pytest configuration and fixtures."""
import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from website import create_app

@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test_key',
        'WTF_CSRF_ENABLED': False,
    })
    
    # Import routes after app creation to avoid circular imports
    from website.routes import main
    app.register_blueprint(main)
    
    # Create test directories
    os.makedirs('website/static', exist_ok=True)
    
    # Create a test audio file
    test_audio_path = os.path.join('website/static', "test_audio.mp3")
    if not os.path.exists(test_audio_path):
        with open(test_audio_path, "wb") as f:
            f.write(b"test audio content")
    
    yield app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for testing yt-dlp commands."""
    with patch('subprocess.run') as mock_run:
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Test Video Title"
        mock_run.return_value = mock_process
        yield mock_run

@pytest.fixture
def mock_openai_transcribe():
    """Mock OpenAI transcription API."""
    with patch('openai.audio.transcriptions.create') as mock_transcribe:
        mock_response = MagicMock()
        mock_response.text = "This is a test transcription."
        mock_transcribe.return_value = mock_response
        yield mock_transcribe

@pytest.fixture
def mock_openai_summarize():
    """Mock OpenAI chat completion API for summarization."""
    with patch('openai.chat.completions.create') as mock_summarize:
        mock_choice = MagicMock()
        mock_choice.message = MagicMock()
        mock_choice.message.content = "This is a test summary."
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_summarize.return_value = mock_response
        yield mock_summarize

@pytest.fixture
def mock_os_path_exists():
    """Mock os.path.exists to always return True."""
    with patch('os.path.exists', return_value=True) as mock_exists:
        yield mock_exists

@pytest.fixture
def mock_os_path_getsize():
    """Mock os.path.getsize to return a valid file size."""
    with patch('os.path.getsize', return_value=1024 * 1024) as mock_getsize:
        yield mock_getsize

@pytest.fixture
def mock_open_file():
    """Mock open function for file operations."""
    mock_file = MagicMock()
    mock_file.__enter__.return_value = mock_file
    
    with patch('builtins.open', return_value=mock_file) as mock_open:
        yield mock_open