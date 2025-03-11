"""Unit tests for API routes."""
import json
import pytest
from flask import url_for

class TestApiRoutes:
    """Test API routes functionality."""
    
    def test_api_process_video_success(self, client, mock_extract_video_id, mock_download_audio, 
                                      mock_transcribe_audio, mock_summarize_text):
        """Test successful API processing of a video."""
        mock_extract_video_id.return_value = "test_video_id"
        mock_download_audio.return_value = ("/fake/path/audio.mp3", "Test Video Title")
        mock_transcribe_audio.return_value = "This is a test transcript."
        mock_summarize_text.return_value = "This is a test summary."
        
        response = client.post(
            '/api/process',
            data=json.dumps({"youtube_url": "https://www.youtube.com/watch?v=test_video_id"}),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data["video_id"] == "test_video_id"
        assert data["video_title"] == "Test Video Title"
        assert data["transcript"] == "This is a test transcript."
        assert data["summary"] == "This is a test summary."
    
    def test_api_process_missing_url(self, client):
        """Test API processing with missing URL."""
        response = client.post(
            '/api/process',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "error" in data
        assert "Please provide a YouTube URL" in data["error"]
    
    def test_api_process_invalid_url(self, client, mock_extract_video_id):
        """Test API processing with invalid URL."""
        mock_extract_video_id.return_value = None
        
        response = client.post(
            '/api/process',
            data=json.dumps({"youtube_url": "https://www.example.com/not-youtube"}),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "error" in data
        assert "Invalid YouTube URL" in data["error"]
    
    def test_api_process_download_failure(self, client, mock_extract_video_id, mock_download_audio):
        """Test API processing with download failure."""
        mock_extract_video_id.return_value = "test_video_id"
        mock_download_audio.return_value = (None, None)
        
        response = client.post(
            '/api/process',
            data=json.dumps({"youtube_url": "https://www.youtube.com/watch?v=test_video_id"}),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert response.status_code == 500
        assert "error" in data
        assert "Failed to download audio" in data["error"]
    
    def test_api_process_transcription_failure(self, client, mock_extract_video_id, 
                                              mock_download_audio, mock_transcribe_audio):
        """Test API processing with transcription failure."""
        mock_extract_video_id.return_value = "test_video_id"
        mock_download_audio.return_value = ("/fake/path/audio.mp3", "Test Video Title")
        mock_transcribe_audio.return_value = None
        
        response = client.post(
            '/api/process',
            data=json.dumps({"youtube_url": "https://www.youtube.com/watch?v=test_video_id"}),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert response.status_code == 500
        assert "error" in data
        assert "Failed to transcribe" in data["error"]