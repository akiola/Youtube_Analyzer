"""Tests for the download_transcript function."""
import pytest
from unittest.mock import patch

def test_download_transcript_file_exists(client, mock_os_path_exists):
    """Test downloading transcript when file exists."""
    mock_os_path_exists.return_value = True
    
    with patch('website.routes.send_file', return_value='file response'):
        response = client.get('/download/test_video_id')
        assert response.status_code != 302

def test_download_transcript_file_not_found(client, mock_os_path_exists):
    """Test downloading transcript when file doesn't exist."""
    mock_os_path_exists.return_value = False
    
    response = client.get('/download/test_video_id')
    assert response.status_code == 302  