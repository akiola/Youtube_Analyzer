"""Tests for the get_video_title function."""
import pytest
from unittest.mock import patch, MagicMock
from website.routes import get_video_title

def test_get_video_title_success():
    """Test get_video_title with successful subprocess execution."""
    with patch('subprocess.run') as mock_run:
        mock_process = MagicMock()
        mock_process.stdout = "Test Video Title\n"
        mock_run.return_value = mock_process
        
        title = get_video_title("dQw4w9WgXcQ")
        
        assert title == "Test Video Title"
        mock_run.assert_called_once()

def test_get_video_title_failure():
    """Test get_video_title with subprocess failure."""
    with patch('subprocess.run', side_effect=Exception("Command failed")):
        title = get_video_title("dQw4w9WgXcQ")
        
        assert title == "Unknown Video"