import jwt
from datetime import datetime, timedelta
from typing import Dict, Any
from src.config.settings import Config

class TokenService:
    def __init__(self):
        self.secret_key = Config.JWT_SECRET_KEY
        self.token_expiration = Config.JWT_ACCESS_TOKEN_EXPIRES
        
    def generate_token(self, payload: Dict[str, Any]) -> str:
        """Gera um token JWT"""
        token_data = {
            **payload,
            'exp': datetime.utcnow() + timedelta(seconds=self.token_expiration),
            'iat': datetime.utcnow()
        }
        return jwt.encode(token_data, self.secret_key, algorithm='HS256')
        
    def validate_token(self, token: str) -> Dict[str, Any]:
        """Valida e decodifica um token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError:
            raise ValueError("Token inválido")