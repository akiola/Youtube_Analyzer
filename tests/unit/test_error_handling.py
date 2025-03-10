"""Tests for error handling in routes."""
import pytest
from unittest.mock import patch, MagicMock

@patch('website.routes.os.path.exists')
def test_download_transcript_file_not_exists_detailed(mock_exists, client):
    """Detailed test for download_transcript when file doesn't exist."""
    mock_exists.return_value = False
    
    with patch('website.routes.flash') as mock_flash:
        response = client.get('/download/test_video_id')
        
        assert response.status_code == 302  
        mock_flash.assert_called_once_with('Transcript file not found')

@patch('website.routes.extract_video_id', return_value="test_id")
@patch('website.routes.download_audio', return_value=(None, None))
def test_process_video_download_failure_detailed(mock_download, mock_extract, client):
    """Detailed test for process_video when download fails."""
    with patch('website.routes.flash') as mock_flash:
        response = client.post('/process', data={'youtube_url': 'https://www.youtube.com/watch?v=test_id'})
        
        assert response.status_code == 302 
        mock_flash.assert_called_once_with('Failed to download audio from the video')

@patch('website.routes.extract_video_id', return_value="test_id")
@patch('website.routes.download_audio', return_value=('/path/to/audio.mp3', 'Test Video'))
@patch('website.routes.transcribe_audio', return_value=None)
def test_process_video_transcribe_failure_detailed(mock_transcribe, mock_download, mock_extract, client):
    """Detailed test for process_video when transcription fails."""
    with patch('website.routes.flash') as mock_flash:
        response = client.post('/process', data={'youtube_url': 'https://www.youtube.com/watch?v=test_id'})
        
        assert response.status_code == 302 
        mock_flash.assert_called_once_with('Failed to transcribe the audio')

@patch('website.routes.extract_video_id', return_value="test_id")
@patch('website.routes.download_audio', return_value=('/path/to/audio.mp3', 'Test Video'))
@patch('website.routes.transcribe_audio', return_value=None)
def test_api_process_video_transcribe_failure_detailed(mock_transcribe, mock_download, mock_extract, client):
    """Detailed test for API route when transcription fails."""
    response = client.post('/api/process', 
                          json={'youtube_url': 'https://www.youtube.com/watch?v=test_id'},
                          content_type='application/json')
    
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert 'Failed to transcribe the audio' in data['error']