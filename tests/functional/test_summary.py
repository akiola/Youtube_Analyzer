"""Final tests to reach 95% coverage."""
import pytest
from unittest.mock import patch, MagicMock

@patch('website.routes.extract_video_id', return_value='test_video_id')
@patch('website.routes.download_audio')
def test_process_video_transcribe_size_limit(mock_download, mock_extract, client):
    """Test process_video when transcription fails due to file size limits."""
    mock_download.return_value = ('test_audio.mp3', 'Test Video')
    
    with patch('website.routes.transcribe_audio', 
               return_value="File too large for transcription. Please try a shorter video."):
        with patch('website.routes.render_template', return_value='rendered template'):
            response = client.post('/process', 
                                  data={'youtube_url': 'https://www.youtube.com/watch?v=test_video_id'})
            
            assert response.status_code == 200

@patch('website.routes.extract_video_id', return_value='test_video_id')
@patch('website.routes.download_audio')
def test_api_process_transcribe_size_limit(mock_download, mock_extract, client):
    """Test API route when transcription returns a size limit message."""
    mock_download.return_value = ('test_audio.mp3', 'Test Video')
    
    with patch('website.routes.transcribe_audio', 
               return_value="File too large for transcription. Please try a shorter video."):
        response = client.post('/api/process', 
                              json={'youtube_url': 'https://www.youtube.com/watch?v=test_video_id'},
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert "File too large" in data.get('transcript', '')

def test_process_video_all_paths_covered(client):
    """Test to ensure all paths in the process_video route are covered."""
    response = client.post('/process', data={})
    assert response.status_code == 302  
    
    with patch('website.routes.extract_video_id', return_value=None):
        response = client.post('/process', data={'youtube_url': 'invalid'})
        assert response.status_code == 302  
    
    with patch('website.routes.extract_video_id', return_value='test_id'), \
         patch('website.routes.download_audio', return_value=(None, None)):
        response = client.post('/process', data={'youtube_url': 'https://www.youtube.com/watch?v=test_id'})
        assert response.status_code == 302 
    
    with patch('website.routes.extract_video_id', return_value='test_id'), \
         patch('website.routes.download_audio', return_value=('test.mp3', 'Test')), \
         patch('website.routes.transcribe_audio', return_value=None):
        response = client.post('/process', data={'youtube_url': 'https://www.youtube.com/watch?v=test_id'})
        assert response.status_code == 302 