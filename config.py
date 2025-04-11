import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'myuser')}:{os.getenv('DB_PASSWORD', 'mypassword')}"
        f"@mysql:3306/{os.getenv('DB_NAME', 'cuidar_plus_bd')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "sua_chave_secreta"
    ENV = "development"  # Altere para 'production' em produção
    SWAGGER = {
        "title": "API Cuidar+",
        "uiversion": 3,
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
    }
    CORS_RESOURCES = {
        r"/*": {
            "origins": [
                "http://localhost:4200",
                "http://127.0.0.1:4200",
                "http://localhost:5001",
                "http://127.0.0.1:5001",
                "http://localhost:5000",
                "http://127.0.0.1:5000",
                "http://127.0.0.1:8080",
                "http://localhost:8080",
            ],  # Permitir apenas este domínio
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type", "X-Test-Environment"],
            "supports_credentials": True,
        }
    }
