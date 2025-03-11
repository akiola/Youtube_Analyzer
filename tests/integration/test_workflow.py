"""Integration tests for the full workflow from YouTube URL to summary."""
import pytest
import json
from unittest.mock import patch, MagicMock

class TestIntegrationWorkflow:
    """Test the integration of the entire workflow."""
    
    @pytest.mark.integration
    def test_full_web_workflow(self, client):
        """Test the full workflow from URL submission to result page."""
        # Mock all the external dependencies
        with patch('website.routes.extract_video_id', return_value="test_video_id"), \
             patch('website.routes.download_audio', return_value=("/fake/path/audio.mp3", "Integration Test Video")), \
             patch('website.routes.transcribe_audio', return_value="This is a transcript from the integration test."), \
             patch('website.routes.summarize_text', return_value="This is a summary from the integration test."):
            
            # Submit the form with a YouTube URL
            response = client.post(
                '/process',
                data={"youtube_url": "https://www.youtube.com/watch?v=test_video_id"},
                follow_redirects=False
            )
            
            # Verify that we get the result page with the correct content
            assert response.status_code == 200
            assert b'Integration Test Video' in response.data
            assert b'This is a transcript from the integration test' in response.data
            assert b'This is a summary from the integration test' in response.data
    
    @pytest.mark.integration
    def test_full_api_workflow(self, client):
        """Test the full API workflow from URL submission to JSON response."""
        # Mock all the external dependencies
        with patch('website.routes.extract_video_id', return_value="test_video_id"), \
             patch('website.routes.download_audio', return_value=("/fake/path/audio.mp3", "Integration Test Video")), \
             patch('website.routes.transcribe_audio', return_value="This is a transcript from the integration test."), \
             patch('website.routes.summarize_text', return_value="This is a summary from the integration test."):
            
            # Submit the API request with a YouTube URL
            response = client.post(
                '/api/process',
                data=json.dumps({"youtube_url": "https://www.youtube.com/watch?v=test_video_id"}),
                content_type='application/json'
            )
            
            # Verify that we get the correct JSON response
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["video_id"] == "test_video_id"
            assert data["video_title"] == "Integration Test Video"
            assert data["transcript"] == "This is a transcript from the integration test."
            assert data["summary"] == "This is a summary from the integration test."
    
    '''@pytest.mark.integration
    def test_download_after_processing(self, client):
        """Test downloading the transcript after processing a video."""
        # Create a class to mock send_file to avoid errors
        class MockResponse:
            def __init__(self):
                self.data = b"mocked file content"
                self.status_code = 200
                self.headers = {}
                
        # Mock file existence and processing
        with patch('os.path.exists', return_value=True), \
             patch('flask.send_file', return_value=MockResponse()), \
             patch('website.routes.extract_video_id', return_value="test_video_id"), \
             patch('website.routes.download_audio', return_value=("/fake/path/audio.mp3", "Integration Test Video")), \
             patch('website.routes.transcribe_audio', return_value="This is a transcript from the integration test."), \
             patch('website.routes.summarize_text', return_value="This is a summary from the integration test."):
            
            # First process a video
            client.post(
                '/process',
                data={"youtube_url": "https://www.youtube.com/watch?v=test_video_id"},
                follow_redirects=False
            )
            
            # Then try to download the transcript
            response = client.get('/download/test_video_id', follow_redirects=False)
            
            # Simple check that we didn't get redirected (which would mean file not found)
            assert response.status_code != 302'''
