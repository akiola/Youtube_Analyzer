"""Common fixtures for all tests."""
import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from website import create_app

@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'  # Add a secret key for testing
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    yield app

@pytest.fixture
def client(app):
    """Create a test client."""
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Set environment variables for testing."""
    original_openai_key = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-dummy-api-key-for-testing"
    yield
    if original_openai_key:
        os.environ["OPENAI_API_KEY"] = original_openai_key
    else:
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

@pytest.fixture
def mock_os_path_exists():
    """Mock os.path.exists function."""
    with patch('os.path.exists') as mock:
        yield mock

@pytest.fixture
def mock_send_file():
    """Mock send_file function."""
    with patch('flask.send_file') as mock:
        yield mock

@pytest.fixture
def mock_download_audio():
    """Mock download_audio function."""
    with patch('website.routes.download_audio') as mock:
        mock.return_value = ('/fake/path/to/audio.mp3', 'Test Video Title')
        yield mock

@pytest.fixture
def mock_transcribe_audio():
    """Mock transcribe_audio function."""
    with patch('website.routes.transcribe_audio') as mock:
        mock.return_value = "This is a test transcript."
        yield mock

@pytest.fixture
def mock_summarize_text():
    """Mock summarize_text function."""
    with patch('website.routes.summarize_text') as mock:
        mock.return_value = "This is a test summary."
        yield mock

@pytest.fixture
def mock_extract_video_id():
    """Mock extract_video_id function."""
    with patch('website.routes.extract_video_id') as mock:
        mock.return_value = 'test_video_id'
        yield mock

@pytest.fixture
def mock_get_video_title():
    """Mock get_video_title function."""
    with patch('website.routes.get_video_title') as mock:
        mock.return_value = 'Test Video Title'
        yield mock

@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run function."""
    with patch('subprocess.run') as mock:
        mock_process = MagicMock()
        mock_process.stdout = "Test Video Title"
        mock_process.returncode = 0
        mock.return_value = mock_process
        yield mock

@pytest.fixture
def mock_open_file():
    """Mock built-in open function."""
    mock_file = MagicMock()
    mock_file.__enter__.return_value = mock_file
    
    with patch('builtins.open', return_value=mock_file) as mock:
        yield mock, mock_file

@pytest.fixture
def mock_openai_transcribe():
    """Mock OpenAI transcription API."""
    with patch('openai.audio.transcriptions.create') as mock:
        mock.return_value = MagicMock(text="This is a mocked transcript")
        yield mock

@pytest.fixture
def mock_openai_summarize():
    """Mock OpenAI chat completion API for summarization."""
    mock_choice = MagicMock()
    mock_choice.message.content = "This is a mocked summary"
    
    with patch('openai.chat.completions.create') as mock:
        mock.return_value = MagicMock(choices=[mock_choice])
        yield mock