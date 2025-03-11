"""Functional tests for web routes."""
import pytest
from flask import url_for

class TestWebRoutes:
    """Test web routes functionality."""
    
    def test_index_route(self, client):
        """Test the index route returns the main page."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_process_video_success(self, client, mock_extract_video_id, mock_download_audio, 
                                  mock_transcribe_audio, mock_summarize_text):
        """Test successful video processing web route."""
        mock_extract_video_id.return_value = "test_video_id"
        mock_download_audio.return_value = ("/fake/path/audio.mp3", "Test Video Title")
        mock_transcribe_audio.return_value = "This is a test transcript."
        mock_summarize_text.return_value = "This is a test summary."
        
        response = client.post(
            '/process',
            data={"youtube_url": "https://www.youtube.com/watch?v=test_video_id"},
            follow_redirects=False
        )
        
        assert response.status_code == 200
        assert b'Test Video Title' in response.data
        assert b'This is a test transcript' in response.data
        assert b'This is a test summary' in response.data
    
    def test_process_video_missing_url(self, client):
        """Test video processing with missing URL."""
        response = client.post(
            '/process',
            data={},
            follow_redirects=True
        )
        
        assert response.status_code == 200  # Redirected to index
        assert b'Please enter a YouTube URL' in response.data
    
    def test_process_video_invalid_url(self, client, mock_extract_video_id):
        """Test video processing with invalid URL."""
        mock_extract_video_id.return_value = None
        
        response = client.post(
            '/process',
            data={"youtube_url": "https://www.example.com/not-youtube"},
            follow_redirects=True
        )
        
        assert response.status_code == 200  # Redirected to index
        assert b'Invalid YouTube URL' in response.data
    
    def test_process_video_download_failure(self, client, mock_extract_video_id, mock_download_audio):
        """Test video processing with download failure."""
        mock_extract_video_id.return_value = "test_video_id"
        mock_download_audio.return_value = (None, None)
        
        response = client.post(
            '/process',
            data={"youtube_url": "https://www.youtube.com/watch?v=test_video_id"},
            follow_redirects=True
        )
        
        assert response.status_code == 200  # Redirected to index
        assert b'Failed to download audio' in response.data
    
    def test_process_video_transcription_failure(self, client, mock_extract_video_id, 
                                               mock_download_audio, mock_transcribe_audio):
        """Test video processing with transcription failure."""
        mock_extract_video_id.return_value = "test_video_id"
        mock_download_audio.return_value = ("/fake/path/audio.mp3", "Test Video Title")
        mock_transcribe_audio.return_value = None
        
        response = client.post(
            '/process',
            data={"youtube_url": "https://www.youtube.com/watch?v=test_video_id"},
            follow_redirects=True
        )
        
        assert response.status_code == 200  # Redirected to index
        assert b'Failed to transcribe' in response.data