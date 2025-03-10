"""Tests for the application factory."""
import pytest
from unittest.mock import patch
from website import create_app

def test_create_app():
    """Test that create_app returns a Flask app."""
    app = create_app()
    assert app is not None
    
    app.secret_key = 'test_key'
    assert app.secret_key is not None

def test_create_app_registers_blueprints():
    """Test that create_app registers the blueprint."""
    app = create_app()
    
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert '/' in rules
    assert '/process' in rules
    assert '/download/<video_id>' in rules
    assert '/api/process' in rules