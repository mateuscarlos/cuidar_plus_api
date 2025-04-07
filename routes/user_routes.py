from flask import Flask, Blueprint, request, jsonify
from models.user import User
from db import db
from flasgger import Swagger
import re
import bleach
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from utils import validate_cpf, sanitize_input
import requests

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

@user_routes.route('/users', methods=['POST'])
def create_user():
    """
    Cria um novo usuário e consulta o endereço via API ViaCEP.
    """
    data = request.get_json()
    try:
        # Consulta o CEP na API ViaCEP
        cep = data.get('cep')
        if not cep:
            return jsonify({'error': 'CEP é obrigatório'}), 400

        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        response.raise_for_status()
        endereco_data = response.json()

        if 'erro' in endereco_data:
            return jsonify({'error': 'CEP não encontrado'}), 404

        # Cria o usuário
        user = User(
            nome=data.get('nome'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            cargo=data.get('cargo'),
            cpf=data.get('cpf'),
            setor=data.get('setor'),
            funcao=data.get('funcao'),
            endereco=endereco_data  # Salva o endereço como JSON
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Usuário criado com sucesso', 'user': user.to_dict()}), 201

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro ao consultar o serviço de CEP: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar usuário: {str(e)}'}), 500

# Registrar o Blueprint no aplicativo
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)