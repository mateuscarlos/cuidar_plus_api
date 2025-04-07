from flask import Blueprint, request, jsonify
from src.application.services.auth_service import AuthService
from src.config.container import get_container

auth_bp = Blueprint('auth', __name__)
auth_service = get_container().get(AuthService)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email e senha são obrigatórios'}), 400
            
        token, user = auth_service.authenticate(email, password)
        
        if not token:
            return jsonify({'message': 'Credenciais inválidas'}), 401
            
        return jsonify({
            'message': 'Login realizado com sucesso!',
            'token': token,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@auth_bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        result = auth_service.register_user(data)
        
        return jsonify({'message': 'User registered successfully', 'user': result}), 201
        
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500