''' package website '''
from flask import Flask
from website.routes import main

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.register_blueprint(main)

    return app
