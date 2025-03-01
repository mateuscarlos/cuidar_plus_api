import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "users.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        'title': 'API Cuidar+',
        'uiversion': 3,
        'debug': True
    }
    CORS_RESOURCES = {r"/api/*": {"origins": "http://127.0.0.1:5000"}}