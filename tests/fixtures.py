"""Shared test fixtures and mocks for more complex scenarios."""
import json
from unittest.mock import MagicMock

class MockFlaskResponse:
    """Mock a Flask response for testing."""
    def __init__(self, data=None, status_code=200, headers=None):
        self.data = data or b""
        self.status_code = status_code
        self.headers = headers or {}
        
    def get_data(self, as_text=False):
        """Get the response data."""
        if as_text and isinstance(self.data, bytes):
            return self.data.decode('utf-8')
        return self.data

class MockOpenAITranscriptionResponse:
    """Mock OpenAI transcription API response."""
    def __init__(self, text="This is a mocked transcript"):
        self.text = text

class MockOpenAICompletionResponse:
    """Mock OpenAI chat completion API response."""
    def __init__(self, content="This is a mocked summary"):
        self.choices = [MagicMock()]
        self.choices[0].message = MagicMock()
        self.choices[0].message.content = content

class MockSubprocessResult:
    """Mock subprocess.run result."""
    def __init__(self, stdout="Test output", stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

def create_mock_api_response(status_code=200, **data):
    """Create a mock API response."""
    response = MockFlaskResponse(
        data=json.dumps(data).encode('utf-8'),
        status_code=status_code,
        headers={"Content-Type": "application/json"}
    )
    return response