from flask import Flask, Blueprint, request, jsonify
from models.user import User
from infrastructure.database.db_config import db
from flasgger import Swagger
import re
import bleach
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from infrastructure.utils.validators import validate_cpf, sanitize_input
from src.application.services.user_service import UserService
from src.interfaces.api.middlewares.auth import token_required
from src.config.container import get_container

# Inicialização do Flask
app = Flask(__name__)

# Configuração do Flasgger (Swagger)
app.config['SWAGGER'] = {
    'title': 'API de Usuários',
    'description': 'API para gerenciamento de usuários',
    'version': '1.0',
    'uiversion': 3,
    'specs_route': '/docs/'  # Rota para acessar a documentação Swagger
}
swagger = Swagger(app)

# Blueprint para as rotas de usuário
user_routes = Blueprint('user_routes', __name__)
user_service = get_container().get(UserService)

@user_routes.route('/api/criar_usuario', methods=['POST'])
@token_required(admin_required=True)
def create_user():
    try:
        data = request.get_json()
        result = user_service.create_user(data)
        return jsonify({'message': 'Usuário criado com sucesso!', 'user': result}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@user_routes.route('/api/exibe_usuarios', methods=['GET'])
@token_required()
def get_all_users():
    try:
        users = user_service.get_all_users()
        return jsonify({'usuarios': users}), 200
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@user_routes.route('/api/atualizar_usuario/<string:cpf>', methods=['PUT'])
@token_required(admin_required=True)
def update_user(cpf):
    try:
        data = request.get_json()
        user_service.update_user(cpf, data)
        return jsonify({'message': 'Usuário atualizado com sucesso!'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@user_routes.route('/api/excluir_usuario/<string:cpf>', methods=['DELETE'])
@token_required(admin_required=True)
def delete_user(cpf):
    try:
        user_service.delete_user(cpf)
        return jsonify({'message': 'Usuário excluído com sucesso!'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

# Error handlers
@user_routes.errorhandler(BadRequest)
@user_routes.errorhandler(Conflict)
@user_routes.errorhandler(NotFound)
def handle_errors(e):
    return jsonify({
        'message': e.description,
        'error': type(e).__name__
    }), e.code

@user_routes.errorhandler(500)
def handle_internal_error(e):
    return jsonify({
        'message': 'Erro interno no servidor',
        'error': 'InternalServerError'
    }), 500

# Registrar o Blueprint no aplicativo
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)