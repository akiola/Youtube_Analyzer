"""Tests for API routes."""
import json
import pytest
from unittest.mock import patch

def test_api_process_video_empty_url(client):
    """Test API route with empty URL."""
    response = client.post('/api/process', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_api_process_video_invalid_url(client):
    """Test API route with invalid URL."""
    with patch('website.routes.extract_video_id', return_value=None):
        response = client.post('/api/process', 
                              json={'youtube_url': 'invalid_url'},
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

@patch('website.routes.extract_video_id')
@patch('website.routes.download_audio')
@patch('website.routes.transcribe_audio')
@patch('website.routes.summarize_text')
def test_api_process_video_success(mock_summarize, mock_transcribe, mock_download, 
                                  mock_extract, client):
    """Test API route with successful processing."""
    mock_extract.return_value = 'test_video_id'
    mock_download.return_value = ('test_audio.mp3', 'Test Video')
    mock_transcribe.return_value = 'Test transcript'
    mock_summarize.return_value = 'Test summary'
    
    response = client.post('/api/process', 
                          json={'youtube_url': 'https://www.youtube.com/watch?v=test_video_id'},
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['video_id'] == 'test_video_id'
    assert data['video_title'] == 'Test Video'
    assert data['transcript'] == 'Test transcript'
    assert data['summary'] == 'Test summary'

@patch('website.routes.extract_video_id')
@patch('website.routes.download_audio')
def test_api_process_video_download_failure(mock_download, mock_extract, client):
    """Test API route with download failure."""
    mock_extract.return_value = 'test_video_id'
    mock_download.return_value = (None, None)
    
    response = client.post('/api/process',
                          json={'youtube_url': 'https://www.youtube.com/watch?v=test_video_id'},
                          content_type='application/json')
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data