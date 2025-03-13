from flask import Flask, Blueprint, request, jsonify
from models.user import User
from db import db
from flasgger import Swagger
import re
import bleach
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from utils import validate_cpf, sanitize_input

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

@user_routes.route('/api/criar_usuario', methods=['POST'])
def create_user():
    """
    Cria um novo usuário
    ---
    tags:
      - Usuários
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nome
            - cpf
            - setor
            - funcao
          properties:
            nome:
              type: string
              description: Nome do usuário
            cpf:
              type: string
              description: CPF do usuário
            rua:
              type: string
              description: Rua do usuário
            numero:
              type: string
              description: Número do endereço do usuário
            complemento:
              type: string
              description: Complemento do endereço do usuário
            cep:
              type: string
              description: CEP do usuário
            bairro:
              type: string
              description: Bairro do usuário
            cidade:
              type: string
              description: Cidade do usuário
            estado:
              type: string
              description: Estado do usuário
            setor:
              type: string
              description: Setor do usuário
            funcao:
              type: string
              description: Função do usuário
            especialidade:
              type: string
              description: Especialidade do usuário
            registro_categoria:
              type: string
              description: Registro da categoria do usuário
            email:
              type: string
              description: Email do usuário
            telefone:
              type: string
              description: Telefone do usuário
            data_admissao:
              type: string
              format: date
              description: Data de admissão do usuário
            status:
              type: string
              description: Status do usuário
            tipo_acesso:
              type: string
              description: Tipo de acesso do usuário
    responses:
      201:
        description: Usuário criado com sucesso
      400:
        description: Campos obrigatórios faltando ou CPF inválido
      409:
        description: CPF já cadastrado
      500:
        description: Erro interno no servidor
    """
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
            'rua': sanitize_input(data.get('rua'), 100) if data.get('rua') else None,
            'numero': sanitize_input(data.get('numero'), 10) if data.get('numero') else None,
            'complemento': sanitize_input(data.get('complemento'), 50) if data.get('complemento') else None,
            'cep': sanitize_input(data.get('cep'), 8) if data.get('cep') else None,
            'bairro': sanitize_input(data.get('bairro'), 50) if data.get('bairro') else None,
            'cidade': sanitize_input(data.get('cidade'), 50) if data.get('cidade') else None,
            'estado': sanitize_input(data.get('estado'), 2) if data.get('estado') else None,
            'setor': sanitize_input(data['setor'], 50),
            'funcao': sanitize_input(data['funcao'], 50),
            'especialidade': sanitize_input(data.get('especialidade'), 50) if data.get('especialidade') else None,
            'registro_categoria': sanitize_input(data.get('registro_categoria'), 50) if data.get('registro_categoria') else None,
            'email': sanitize_input(data.get('email'), 100) if data.get('email') else None,
            'telefone': sanitize_input(data.get('telefone'), 15) if data.get('telefone') else None,
            'data_admissao': data.get('data_admissao'),
            'status': sanitize_input(data.get('status'), 20) if data.get('status') else None,
            'tipo_acesso': sanitize_input(data.get('tipo_acesso'), 20) if data.get('tipo_acesso') else None
        }

        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': 'Usuário criado com sucesso!',
            'id': new_user.id
        }), 201

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except Conflict as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500

@user_routes.route('/api/exibe_usuarios', methods=['GET'])
def get_all_users():
    """
    Exibe todos os usuários
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários
      500:
        description: Erro ao recuperar usuários
    """
    try:
        # Busca todos os usuários sem paginação
        usuarios = User.query.all()

        # Retorna a lista de usuários
        return jsonify({
            'usuarios': [{
                'id': u.id,
                'nome': u.nome,
                'cpf': u.cpf,
                'rua': u.rua,
                'numero': u.numero,
                'complemento': u.complemento,
                'cep': u.cep,
                'bairro': u.bairro,
                'cidade': u.cidade,
                'estado': u.estado,
                'setor': u.setor,
                'funcao': u.funcao,
                'especialidade': u.especialidade,
                'registro_categoria': u.registro_categoria,
                'email': u.email,
                'telefone': u.telefone,
                'data_admissao': u.data_admissao,
                'status': u.status,
                'tipo_acesso': u.tipo_acesso
            } for u in usuarios]
        }), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao recuperar usuários', 'error': str(e)}), 500

@user_routes.route('/api/atualizar_usuario/<cpf>', methods=['PUT'])
def atualizar_usuario(cpf):
    """
    Atualiza um usuário existente
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: cpf
        type: string
        required: true
        description: CPF do usuário
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome:
              type: string
              description: Nome do usuário
            rua:
              type: string
              description: Rua do usuário
            numero:
              type: string
              description: Número do endereço do usuário
            complemento:
              type: string
              description: Complemento do endereço do usuário
            cep:
              type: string
              description: CEP do usuário
            bairro:
              type: string
              description: Bairro do usuário
            cidade:
              type: string
              description: Cidade do usuário
            estado:
              type: string
              description: Estado do usuário
            setor:
              type: string
              description: Setor do usuário
            funcao:
              type: string
              description: Função do usuário
            especialidade:
              type: string
              description: Especialidade do usuário
            registro_categoria:
              type: string
              description: Registro da categoria do usuário
            email:
              type: string
              description: Email do usuário
            telefone:
              type: string
              description: Telefone do usuário
            data_admissao:
              type: string
              format: date
              description: Data de admissão do usuário
            status:
              type: string
              description: Status do usuário
            tipo_acesso:
              type: string
              description: Tipo de acesso do usuário
    responses:
      200:
        description: Usuário atualizado com sucesso
      400:
        description: CPF inválido
      404:
        description: Usuário não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        usuario = User.query.filter_by(cpf=cpf).first()
        if not usuario:
            raise NotFound("Usuário não encontrado")

        data = request.get_json()
        update_fields = {
            'nome': sanitize_input(data.get('nome'), 100) if data.get('nome') else None,
            'rua': sanitize_input(data.get('rua'), 100) if data.get('rua') else None,
            'numero': sanitize_input(data.get('numero'), 10) if data.get('numero') else None,
            'complemento': sanitize_input(data.get('complemento'), 50) if data.get('complemento') else None,
            'cep': sanitize_input(data.get('cep'), 8) if data.get('cep') else None,
            'bairro': sanitize_input(data.get('bairro'), 50) if data.get('bairro') else None,
            'cidade': sanitize_input(data.get('cidade'), 50) if data.get('cidade') else None,
            'estado': sanitize_input(data.get('estado'), 2) if data.get('estado') else None,
            'setor': sanitize_input(data.get('setor'), 50) if data.get('setor') else None,
            'funcao': sanitize_input(data.get('funcao'), 50) if data.get('funcao') else None,
            'especialidade': sanitize_input(data.get('especialidade'), 50) if data.get('especialidade') else None,
            'registro_categoria': sanitize_input(data.get('registro_categoria'), 50) if data.get('registro_categoria') else None,
            'email': sanitize_input(data.get('email'), 100) if data.get('email') else None,
            'telefone': sanitize_input(data.get('telefone'), 15) if data.get('telefone') else None,
            'data_admissao': data.get('data_admissao'),
            'status': sanitize_input(data.get('status'), 20) if data.get('status') else None,
            'tipo_acesso': sanitize_input(data.get('tipo_acesso'), 20) if data.get('tipo_acesso') else None
        }

        for key, value in update_fields.items():
            if value is not None:
                setattr(usuario, key, value)
        
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso!'}), 200

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500

@user_routes.route('/api/excluir_usuario/<cpf>', methods=['DELETE'])
def excluir_usuario(cpf):
    """
    Exclui um usuário existente
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: cpf
        type: string
        required: true
        description: CPF do usuário
    responses:
      200:
        description: Usuário excluído com sucesso
      400:
        description: CPF inválido
      404:
        description: Usuário não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        usuario = User.query.filter_by(cpf=cpf).first()
        if not usuario:
            raise NotFound("Usuário não encontrado")
        
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso!'}), 200

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500

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