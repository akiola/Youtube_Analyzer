"""Functional tests for transcript download feature."""
import pytest

class TestDownloadTranscript:    
    
    def test_download_transcript_file_not_found(self, client, mock_os_path_exists):
        """Test downloading transcript when file doesn't exist."""
        mock_os_path_exists.return_value = False
        
        response = client.get('/download/test_video_id')
        
        # Should redirect to index with flash message
        assert response.status_code == 302
        
        # Follow the redirect to check the flash message
        response = client.get('/download/test_video_id', follow_redirects=True)
        assert b'Transcript file not found' in response.data
        