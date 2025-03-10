"""Tests to push coverage to 95% or higher."""
import pytest
from unittest.mock import patch, MagicMock


@patch('website.routes.extract_video_id')
@patch('website.routes.download_audio')
@patch('website.routes.transcribe_audio')
@patch('website.routes.summarize_text')
def test_process_video_complete_flow(mock_summarize, mock_transcribe, mock_download, mock_extract, client):
    """Test the complete flow of process_video with all steps mocked."""
    mock_extract.return_value = 'test_video_id'
    mock_download.return_value = ('test_audio.mp3', 'Test Video')
    mock_transcribe.return_value = 'Test transcript'
    mock_summarize.return_value = 'Test summary'
    
    with patch('website.routes.render_template', return_value='rendered template') as mock_render:
        response = client.post('/process', data={'youtube_url': 'https://www.youtube.com/watch?v=test_video_id'})
        
        mock_extract.assert_called_once()
        mock_download.assert_called_once()
        mock_transcribe.assert_called_once()
        mock_summarize.assert_called_once()
        mock_render.assert_called_once()

@patch('website.routes.os.path.exists')
def test_download_transcript_with_send_file(mock_exists, client):
    """Test downloading transcript with send_file handling."""
    mock_exists.return_value = True
    
    with patch('website.routes.send_file', side_effect=lambda path, **kwargs: f"Sending file: {path}") as mock_send:
        response = client.get('/download/test_video_id')
        
        mock_send.assert_called_once()
        
        args, kwargs = mock_send.call_args
        assert "transcription.txt" in args[0] or "test_video_id" in args[0]
        assert kwargs.get('as_attachment') is True

@patch('website.routes.extract_video_id', return_value=None)
def test_api_process_invalid_url_detailed(mock_extract, client):
    """Test API processing with an invalid URL - more detailed."""
    response = client.post('/api/process',
                          json={'youtube_url': 'invalid_url'},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid YouTube URL'
    mock_extract.assert_called_once()

@patch('website.routes.extract_video_id', return_value="test_video_id")
@patch('website.routes.download_audio', return_value=(None, None))
def test_api_process_download_failure_detailed(mock_download, mock_extract, client):
    """Test API processing with download failure - more detailed."""
    response = client.post('/api/process',
                          json={'youtube_url': 'https://www.youtube.com/watch?v=test_video_id'},
                          content_type='application/json')
    
    assert response.status_code == 500
    data = response.get_json()
    assert data['error'] == 'Failed to download audio from the video'
    mock_extract.assert_called_once()
    mock_download.assert_called_once()