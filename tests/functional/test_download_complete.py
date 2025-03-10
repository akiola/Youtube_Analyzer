"""Comprehensive tests for download functions."""
import os
import pytest
from unittest.mock import patch, MagicMock, mock_open
from website.routes import download_audio, get_video_title, STATIC_DIR

@pytest.fixture
def mock_static_dir():
    """Mock the STATIC_DIR for testing."""
    with patch('website.routes.STATIC_DIR', '/fake/static/dir'):
        yield

@pytest.fixture
def mock_subprocess_complete():
    """Mock for a complete subprocess run call and response."""
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Test output"
        mock_result.stderr = ""
        
        mock_run.return_value = mock_result
        
        yield mock_run

class TestVideoDownload:
    """Tests for video downloading functions."""
    
    def test_get_video_title_complete(self, mock_subprocess_complete):
        """Test the complete get_video_title function."""
        mock_subprocess_complete.return_value.stdout = "My Test Video Title\n"
        
        title = get_video_title("test123")
        
        assert title == "My Test Video Title"
        mock_subprocess_complete.assert_called_once()
        
        args, _ = mock_subprocess_complete.call_args
        command = args[0]
        assert "yt-dlp" in command
        assert "--print" in command
        assert "title" in command
        assert "test123" in command[-1]
    
    def test_download_audio_complete(self, mock_subprocess_complete, mock_static_dir):
        """Test the complete download_audio function."""
        audio_file_path = "/fake/static/dir/video_audio_test123.mp3"
        
        with patch('os.path.join', return_value=audio_file_path), \
             patch('website.routes.get_video_title', return_value="Test Video Title"):
            
            file_path, title = download_audio("test123")
            
            assert file_path == audio_file_path
            assert title == "Test Video Title"
            mock_subprocess_complete.assert_called_once()
            
            args, _ = mock_subprocess_complete.call_args
            command = args[0]
            assert "yt-dlp" in command
            assert "-x" in command
            assert "--audio-format" in command
            assert "mp3" in command
            assert audio_file_path in command
            assert "test123" in command[-1]
    
    def test_download_audio_command_error(self, mock_subprocess_complete, mock_static_dir):
        """Test download_audio function when command returns an error."""
        mock_subprocess_complete.return_value.returncode = 1
        mock_subprocess_complete.return_value.stderr = "Command failed"
        
        with patch('os.path.join', return_value="/fake/path"):
            file_path, title = download_audio("test123")
            
            assert file_path is None
            assert title is None
            mock_subprocess_complete.assert_called_once()
    
    def test_download_audio_exception(self, mock_static_dir):
        """Test download_audio function when an exception occurs."""
        with patch('subprocess.run', side_effect=Exception("Test exception")), \
             patch('os.path.join', return_value="/fake/path"):
            
            file_path, title = download_audio("test123")
            
            assert file_path is None
            assert title is None