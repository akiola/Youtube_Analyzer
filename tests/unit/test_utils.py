"""Tests for utility functions in the routes module."""
import pytest
from unittest.mock import patch, MagicMock
from website.routes import extract_video_id, transcribe_audio, summarize_text

def test_extract_video_id():
    """Test extraction of YouTube video IDs from different URL formats."""
    # Test standard YouTube URL
    assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    
    # Test YouTube short URL
    assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    
    # Test embed URL
    assert extract_video_id("https://www.youtube.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    
    # Test invalid URL
    assert extract_video_id("https://example.com") is None
    
    # Test empty URL
    assert extract_video_id("") is None

@pytest.mark.skip(reason="Needs environment-specific mock")
def test_download_audio():
    """Test downloading audio from YouTube."""
    pass

def test_transcribe_audio(mock_os_path_exists, mock_os_path_getsize, mock_openai_transcribe):
    """Test audio transcription functionality."""
    mock_file = MagicMock()
    m = MagicMock()
    
    with patch('builtins.open', return_value=mock_file):
        result = transcribe_audio("test_audio.mp3")
        assert result == "This is a test transcription."
    
    mock_os_path_exists.return_value = False
    result = transcribe_audio("nonexistent.mp3")
    assert result is None
    
    mock_os_path_exists.return_value = True
    mock_os_path_getsize.return_value = 30 * 1024 * 1024  
    result = transcribe_audio("large_file.mp3")
    assert "File too large" in result

def test_summarize_text(mock_openai_summarize):
    """Test text summarization functionality."""
    result = summarize_text("This is a test transcript.")
    assert result == "This is a test summary."
    
    with patch('openai.chat.completions.create', side_effect=Exception("API error")):
        result = summarize_text("This is a test transcript.")
        assert result is None