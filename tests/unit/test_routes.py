"""Unit tests for functions in routes.py."""
import os
import pytest
from website.routes import extract_video_id, get_video_title, download_audio, transcribe_audio, summarize_text

class TestVideoUrlExtraction:
    """Test the extraction of video IDs from URLs."""
    
    def test_extract_video_id_from_watch_url(self):
        """Test extracting video ID from standard watch URL."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_from_short_url(self):
        """Test extracting video ID from youtu.be URL."""
        url = "https://youtu.be/dQw4w9WgXcQ"
        video_id = extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_from_embed_url(self):
        """Test extracting video ID from embed URL."""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        video_id = extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_from_invalid_url(self):
        """Test extracting video ID from invalid URL."""
        url = "https://www.example.com/watch?v=dQw4w9WgXcQ"
        video_id = extract_video_id(url)
        assert video_id is None

class TestVideoOperations:
    """Test video-related operations."""
    
    def test_get_video_title(self, mock_subprocess_run):
        """Test fetching a video title using yt-dlp."""
        mock_subprocess_run.return_value.stdout = "Test Video Title\n"
        title = get_video_title("test_video_id")
        assert title == "Test Video Title"
        mock_subprocess_run.assert_called_once()
    
    def test_get_video_title_error(self, mock_subprocess_run):
        """Test error handling when fetching video title."""
        mock_subprocess_run.side_effect = Exception("Test error")
        title = get_video_title("test_video_id")
        assert title == "Unknown Video"
    
    def test_download_audio_success(self, mock_subprocess_run, mock_get_video_title):
        """Test downloading audio successfully."""
        mock_subprocess_run.return_value.returncode = 0
        mock_get_video_title.return_value = "Test Video Title"
        
        with patch('os.path.join', return_value="/fake/path/audio.mp3"):
            audio_file, title = download_audio("test_video_id")
            
        assert audio_file == "/fake/path/audio.mp3"
        assert title == "Test Video Title"
        mock_subprocess_run.assert_called_once()
    
    def test_download_audio_failure(self, mock_subprocess_run):
        """Test handling download failure."""
        mock_subprocess_run.return_value.returncode = 1
        mock_subprocess_run.return_value.stderr = "Error downloading"
        
        audio_file, title = download_audio("test_video_id")
        
        assert audio_file is None
        assert title is None
        mock_subprocess_run.assert_called_once()

class TestTranscriptionOperations:
    """Test transcription and summarization operations."""
    
    def test_transcribe_audio_success(self, mock_openai_transcribe, mock_open_file):
        """Test successful audio transcription."""
        mock_file, mock_file_obj = mock_open_file
        
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1024):
            result = transcribe_audio("/fake/path/audio.mp3")
        
        assert result == "This is a mocked transcript"
        mock_openai_transcribe.assert_called_once()
    
    def test_transcribe_audio_file_not_found(self):
        """Test transcription when file doesn't exist."""
        with patch('os.path.exists', return_value=False):
            result = transcribe_audio("/fake/path/audio.mp3")
        
        assert result is None
    
    def test_transcribe_audio_file_too_large(self):
        """Test transcription when file is too large."""
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=30 * 1024 * 1024):  # 30MB
            result = transcribe_audio("/fake/path/audio.mp3")
        
        assert "File too large" in result
    
    def test_summarize_text_success(self, mock_openai_summarize):
        """Test successful text summarization."""
        result = summarize_text("This is a test transcript")
        
        assert result == "This is a mocked summary"
        mock_openai_summarize.assert_called_once()
    
    def test_summarize_text_error(self):
        """Test error handling in summarization."""
        with patch('openai.chat.completions.create', side_effect=Exception("Test error")):
            result = summarize_text("This is a test transcript")
        
        assert result is None

# Required patches to make the above tests work
import unittest.mock as mock
patch = mock.patch