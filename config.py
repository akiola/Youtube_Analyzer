import os

class Config:
    API_KEY = os.getenv('OPENAI_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-replace-in-production')
    