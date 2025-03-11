"""Functional tests for transcript download feature."""
import pytest

class TestDownloadTranscript:
    """Test the download transcript functionality."""
    
    def test_download_transcript_file_exists(self, client, mock_os_path_exists):
        """Test downloading transcript when file exists."""
        mock_os_path_exists.return_value = True
        
        # Create a class to mock send_file to avoid errors
        class MockResponse:
            def __init__(self):
                self.data = b"mocked file content"
                self.status_code = 200
                self.headers = {"Content-Disposition": "attachment; filename=transcription.txt"}
        
        with pytest.MonkeyPatch.context() as mp:
            # Patch send_file to avoid actual file operations
            mp.setattr("flask.send_file", lambda *args, **kwargs: MockResponse())
            response = client.get('/download/test_video_id')
            
            # Check that we don't get redirected (which would happen if file not found)
            assert response.status_code != 302
    
    def test_download_transcript_file_not_found(self, client, mock_os_path_exists):
        """Test downloading transcript when file doesn't exist."""
        mock_os_path_exists.return_value = False
        
        response = client.get('/download/test_video_id')
        
        # Should redirect to index with flash message
        assert response.status_code == 302
        
        # Follow the redirect to check the flash message
        response = client.get('/download/test_video_id', follow_redirects=True)
        assert b'Transcript file not found' in response.data
        