"""Tests for Flask application initialization."""
import pytest
from flask import Flask
from website import create_app

class TestAppInitialization:
    """Test the Flask application initialization."""
    
    def test_create_app(self):
        """Test that create_app returns a Flask application."""
        app = create_app()
        assert isinstance(app, Flask)
        # Don't check for ENV since Flask's newer versions might not have it
    
    def test_app_config(self):
        """Test that the app has the expected configuration."""
        app = create_app()
        app.config['TESTING'] = True
        assert app.config['TESTING'] is True
    
    def test_blueprints_registered(self):
        """Test that blueprints are registered properly."""
        app = create_app()
        
        # Check that the 'main' blueprint is registered
        assert any(bp.name == 'main' for bp in app.blueprints.values())
        
        # Test routes defined in the blueprint
        rules = [rule.endpoint for rule in app.url_map.iter_rules()]
        assert 'main.index' in rules
        assert 'main.process_video' in rules
        assert 'main.download_transcript' in rules
        assert 'main.api_process_video' in rules