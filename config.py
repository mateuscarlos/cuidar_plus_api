import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'myuser')}:{os.getenv('DB_PASSWORD', 'mypassword')}"
        f"@mysql/{os.getenv('DB_NAME', 'cuidar_plus_bd')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        'title': 'API Cuidar+',
        'uiversion': 3,
        'specs': [
            {
                'endpoint': 'apispec_1',
                'route': '/apispec_1.json',
                'rule_filter': lambda rule: True,  # all in
                'model_filter': lambda tag: True,  # all in
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/docs/'
    }
    CORS_RESOURCES = {
        r"/api/*": {
            "origins": ["http://localhost:4200","http://127.0.0.1:5000", "http://127.0.0.1:80", "http://localhost"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Authorization", "Content-Type"],
            }
        }