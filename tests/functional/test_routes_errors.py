"""Tests for error conditions in routes."""
import pytest
from unittest.mock import patch

@patch('website.routes.extract_video_id')
@patch('website.routes.download_audio')
@patch('website.routes.transcribe_audio')
def test_process_video_transcribe_failure(mock_transcribe, mock_download, mock_extract, client):
    """Test process_video route when transcription fails."""
    mock_extract.return_value = 'test_video_id'
    mock_download.return_value = ('test_audio.mp3', 'Test Video')
    mock_transcribe.return_value = None  
    
    response = client.post('/process', data={'youtube_url': 'https://www.youtube.com/watch?v=test_video_id'})
    
    assert response.status_code == 302  

@patch('website.routes.extract_video_id')
@patch('website.routes.download_audio')
@patch('website.routes.transcribe_audio')
@patch('website.routes.summarize_text')
def test_api_process_video_transcribe_failure(mock_summarize, mock_transcribe, mock_download, mock_extract, client):
    """Test API route when transcription fails."""
    mock_extract.return_value = 'test_video_id'
    mock_download.return_value = ('test_audio.mp3', 'Test Video')
    mock_transcribe.return_value = None  
    
    response = client.post('/api/process', 
                          json={'youtube_url': 'https://www.youtube.com/watch?v=test_video_id'},
                          content_type='application/json')
    
    assert response.status_code == 500  

@pytest.mark.parametrize('route,expected_status', [
    ('/nonexistent', 404),
])
def test_route_existence(client, route, expected_status):
    """Test that routes exist or return 404 as appropriate."""
    response = client.get(route)
    assert response.status_code == expected_status

def test_index_route_exists(client):
    """Test that the index route exists but skip template rendering."""
    with patch('website.routes.render_template', return_value='mocked template'):
        response = client.get('/')
        assert response.status_code == 200

def test_method_not_allowed(client):
    """Test that methods are properly restricted."""
    response = client.get('/process')
    assert response.status_code == 405  