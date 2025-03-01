from flask import Flask, Blueprint, request, jsonify
from models.user import User
from db import db
from flasgger import Swagger, swag_from
import re
import bleach
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from utils import validate_cpf, sanitize_input

# Inicialização do Flask
app = Flask(__name__)

# Configurações de segurança
talisman = Talisman(app)
limiter = Limiter(app=app, key_func=get_remote_address)

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

@user_routes.route('/api/criar_usuario', methods=['POST'])
@swag_from('swagger/create_user.yml')
def create_user():
    try:
        data = request.get_json()
        required_fields = ['nome', 'cpf', 'setor', 'funcao']
        if not all(field in data for field in required_fields):
            raise BadRequest("Campos obrigatórios faltando: nome, cpf, setor, funcao")
        
        cpf = re.sub(r'[^\d]', '', data['cpf'])
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        if User.query.filter_by(cpf=cpf).first():
            raise Conflict("CPF já cadastrado")

        user_data = {
            'nome': sanitize_input(data['nome'], 100),
            'cpf': cpf,
            'endereco': sanitize_input(data.get('endereco'), 200),
            'setor': sanitize_input(data['setor'], 50),
            'funcao': sanitize_input(data['funcao'], 50),
            'especialidade': sanitize_input(data.get('especialidade'), 50),
            'registro_categoria': sanitize_input(data.get('registro_categoria'), 20)
        }

        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': 'Usuário criado com sucesso!',
            'matricula': new_user.id
        }), 201

    except ValueError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor'}), 500

@user_routes.route('/api/exibe_usuarios', methods=['GET'])
@swag_from('swagger/get_users.yml')
def get_all_users():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = User.query
        if setor := request.args.get('setor'):
            query = query.filter_by(setor=sanitize_input(setor))
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'usuarios': [{
                'matricula': u.id,
                'nome': u.nome,
                'setor': u.setor,
                'funcao': u.funcao,
                'cpf': u.cpf
            } for u in pagination.items],
            'total': pagination.total,
            'paginas': pagination.pages,
            'pagina_atual': page
        }), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao recuperar usuários'}), 500

@user_routes.route('/api/atualizar_usuario/<cpf>', methods=['PUT'])
@swag_from('swagger/update_user.yml')
def atualizar_usuario(cpf):
    try:
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        usuario = User.query.filter_by(cpf=cpf).first()
        if not usuario:
            raise NotFound("Usuário não encontrado")

        data = request.get_json()
        update_fields = {
            'nome': sanitize_input(data.get('nome'), 100),
            'setor': sanitize_input(data.get('setor'), 50),
            'funcao': sanitize_input(data.get('funcao'), 50),
            'especialidade': sanitize_input(data.get('especialidade'), 50),
            'registro_categoria': sanitize_input(data.get('registro_categoria'), 20)
        }

        for key, value in update_fields.items():
            if value is not None:
                setattr(usuario, key, value)
        
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@user_routes.route('/api/excluir_usuario/<cpf>', methods=['DELETE'])
@swag_from('swagger/delete_user.yml')
def excluir_usuario(cpf):
    try:
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        usuario = User.query.filter_by(cpf=cpf).first()
        if not usuario:
            raise NotFound("Usuário não encontrado")
        
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

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