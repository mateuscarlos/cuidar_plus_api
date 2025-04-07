import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configurações existentes...
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hora
    
    # Configurações de banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://user:password@localhost/cuidar_plus_api')
    SQLALCHEMY_TRACK_MODIFICATIONS = False