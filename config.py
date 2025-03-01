class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        'title': 'API Cuidar+',
        'uiversion': 3,
        'debug': True
    }
    CORS_RESOURCES = {r"/api/*": {"origins": "http://127.0.0.1:5000"}}