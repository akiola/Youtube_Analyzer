import pytest
import json

def test_index(client):
    """Test if the homepage loads successfully."""
    response = client.get("/")
    assert response.status_code == 200

def test_process_invalid_url(client):
    """Test processing with an invalid YouTube URL."""
    response = client.post("/process", data={"youtube_url": "invalid-url"})
    assert response.status_code == 302  

def test_process_video_success(mocker, client):
    """Mock dependencies to test video processing."""
    mocker.patch("website.views.extract_video_id", return_value="test123")
    mocker.patch("website.views.download_audio", return_value=("test_audio.mp3", "Test Video"))
    mocker.patch("website.views.transcribe_audio", return_value="Test transcript.")
    mocker.patch("website.views.summarize_text", return_value="Test summary.")

    response = client.post("/process", data={"youtube_url": "https://youtu.be/test123"})
    assert response.status_code == 200
    assert b"Test Video" in response.data
    assert b"Test transcript." in response.data
    assert b"Test summary." in response.data

def test_api_process_video(client, mocker):
    """Mock API video processing."""
    mocker.patch("website.views.extract_video_id", return_value="test123")
    mocker.patch("website.views.download_audio", return_value=("test_audio.mp3", "Test Video"))
    mocker.patch("website.views.transcribe_audio", return_value="Test transcript.")
    mocker.patch("website.views.summarize_text", return_value="Test summary.")

    response = client.post("/api/process", json={"youtube_url": "https://youtu.be/test123"})
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["video_title"] == "Test Video"
    assert data["transcript"] == "Test transcript."
    assert data["summary"] == "Test summary."

def test_download_transcript(client, mocker):
    """Test downloading the transcript file."""
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="Transcript content."))
    mock_exists = mocker.patch("os.path.exists", return_value=True)

    response = client.get("/download/test123")
    assert response.status_code == 200
    assert response.data == b"Transcript content."
