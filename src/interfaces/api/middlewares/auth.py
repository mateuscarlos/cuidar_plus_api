from functools import wraps
from flask import request, jsonify, g
from src.infrastructure.security.token_service import TokenService
from src.config.container import get_container

def token_required(admin_required=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token_service = get_container().get(TokenService)
            
            # Obter token do cabeçalho
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'message': 'Token de autenticação ausente'}), 401
                
            token = auth_header.split(' ')[1]
            
            try:
                # Validar token
                payload = token_service.validate_token(token)
                
                # Verificar permissões de admin se necessário
                if admin_required and payload.get('tipo_acesso') != 'admin':
                    return jsonify({'message': 'Acesso não autorizado'}), 403
                    
                # Armazenar dados do usuário para uso na rota
                g.user = payload
                
                return f(*args, **kwargs)
                
            except ValueError as e:
                return jsonify({'message': str(e)}), 401
                
        return decorated_function
    return decorator