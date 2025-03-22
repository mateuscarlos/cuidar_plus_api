import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'myuser')}:{os.getenv('DB_PASSWORD', 'mypassword')}"
        f"@mysql:3306/{os.getenv('DB_NAME', 'cuidar_plus_bd')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SWAGGER = {
        'title': 'API Cuidar+',
        'uiversion': 3,
        'specs': [
            {
                'endpoint': 'apispec_1',
                'route': '/apispec_1.json',
                'rule_filter': lambda rule: True, 
                'model_filter': lambda tag: True, 
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/docs/'
    }
    CORS_RESOURCES = {
        r"/api/*": {
            "origins": ["http://localhost:4200","http://127.0.0.1:5000", "http://127.0.0.1:80", "http://localhost", "http://127.0.0.1:5001"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Authorization", "Content-Type"],
            },
        r"/api/update_user/*": {
        "origins": ["http://localhost:4200","http://127.0.0.1:5000", "http://127.0.0.1:80", "http://localhost", "http://127.0.0.1:5001"],
        "methods": ["PUT"],
        "allow_headers": ["Authorization", "Content-Type"],
    }
}