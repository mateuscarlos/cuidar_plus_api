from flask import Flask, Blueprint, request, jsonify
from models.user import User
from db import db
from flasgger import Swagger
import re
import bleach
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from utils import validate_cpf, sanitize_input
import requests
from datetime import datetime

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

import re

def camel_to_snake(data):
    """
    Converte as chaves de um dicionário de camelCase para snake_case.
    """
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
            new_data[new_key] = camel_to_snake(value) if isinstance(value, (dict, list)) else value
        return new_data
    elif isinstance(data, list):
        return [camel_to_snake(item) for item in data]
    else:
        return data

@user_routes.route('/usuarios/criar', methods=['POST'])
def create_user():
    """
    Cria um novo usuário e consulta o endereço via API ViaCEP.
    """
    data = camel_to_snake(request.get_json())  # Converte camelCase para snake_case
    try:
        # Consulta o CEP na API ViaCEP
        cep = data.get('cep')
        if not cep:
            return jsonify({'error': 'CEP é obrigatório'}), 400

        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        response.raise_for_status()
        endereco_via_cep = response.json()

        if 'erro' in endereco_via_cep:
            return jsonify({'error': 'CEP não encontrado'}), 404

        # Mesclar o endereço da API ViaCEP com os dados enviados pelo formulário
        endereco_formulario = data.get('endereco', {})
        endereco_final = {
            # Dados do ViaCEP como referência
            'cep': cep,
            'logradouro': endereco_via_cep.get('logradouro', ''),
            'bairro': endereco_via_cep.get('bairro', ''),
            'localidade': endereco_via_cep.get('localidade', ''),
            'uf': endereco_via_cep.get('uf', ''),
            'estado': endereco_via_cep.get('uf', ''),
            
            # Sobrescrever com dados do formulário que têm prioridade
            'numero': endereco_formulario.get('numero', ''),
            'complemento': endereco_formulario.get('complemento', ''),
        }
        
        # Se houver mais campos no formulário, preservá-los
        if endereco_formulario:
            for key, value in endereco_formulario.items():
                if key not in ['cep'] and key not in endereco_final:
                    endereco_final[key] = value

        # Converte data_admissao para o formato correto (YYYY-MM-DD)
        data_admissao = data.get('data_admissao')
        if data_admissao:
            try:
                data_admissao = datetime.fromisoformat(data_admissao.replace("Z", "")).date()
            except ValueError:
                return jsonify({'error': 'Formato de data_admissao inválido. Use o formato ISO 8601.'}), 400

        # Cria o usuário
        user = User(
            nome=data.get('nome'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            cargo=data.get('cargo'),
            cpf=data.get('cpf'),
            cep=cep,
            setor=data.get('setor'),
            funcao=data.get('funcao'),
            endereco=endereco_final,  # Usando o endereço mesclado
            status=data.get('status'),
            telefone=data.get('telefone'),
            especialidade=data.get('especialidade'),
            registro_categoria=data.get('registro_categoria'),
            data_admissao=data_admissao,  # Valor convertido
            tipo_acesso=data.get('tipo_acesso'),
            tipo_contratacao=data.get('tipo_contratacao'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Usuário criado com sucesso', 'user': user.to_dict()}), 201

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro ao consultar o serviço de CEP: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar usuário: {str(e)}'}), 500

@user_routes.route('/usuarios', methods=['GET'])
def get_all_users():
    """
    Lista todos os usuários cadastrados.
    """
    try:
        usuarios = User.query.all()
        return jsonify([user.to_dict() for user in usuarios]), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar usuários: {str(e)}'}), 500


@user_routes.route('/usuarios/<int:id>', methods=['GET'])
def get_user_by_id(id):
    """
    Retorna os detalhes de um usuário específico pelo ID.
    """
    try:
        user = User.query.get(id)
        if not user:
            raise NotFound('Usuário não encontrado')
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar usuário: {str(e)}'}), 500


@user_routes.route('/usuarios/<int:id>', methods=['PUT'])
def update_user(id):
    """
    Atualiza as informações de um usuário existente.
    """
    data = camel_to_snake(request.get_json())  # Converte camelCase para snake_case
    try:
        user = User.query.get(id)
        if not user:
            raise NotFound('Usuário não encontrado')

        # Atualiza o CEP e consulta o endereço via API ViaCEP
        new_cep = data.get('cep')
        if new_cep and new_cep != user.cep:
            try:
                response = requests.get(f'https://viacep.com.br/ws/{new_cep}/json/')
                response.raise_for_status()
                endereco_via_cep = response.json()

                if 'erro' in endereco_via_cep:
                    return jsonify({'error': 'CEP não encontrado'}), 404
                
                # Mesclar o endereço da API ViaCEP com os dados enviados pelo formulário
                endereco_formulario = data.get('endereco', {})
                endereco_final = {
                    # Dados do ViaCEP como referência
                    'cep': new_cep,
                    'logradouro': endereco_via_cep.get('logradouro', ''),
                    'bairro': endereco_via_cep.get('bairro', ''),
                    'localidade': endereco_via_cep.get('localidade', ''),
                    'uf': endereco_via_cep.get('uf', ''),
                    'estado': endereco_via_cep.get('uf', ''),
                    
                    # Sobrescrever com dados do formulário que têm prioridade
                    'numero': endereco_formulario.get('numero', ''),
                    'complemento': endereco_formulario.get('complemento', '')
                }
                
                # Se houver mais campos no formulário, preservá-los
                if endereco_formulario:
                    for key, value in endereco_formulario.items():
                        if key not in ['cep'] and key not in endereco_final:
                            endereco_final[key] = value

                user.cep = new_cep
                user.endereco = endereco_final
            except requests.exceptions.RequestException as e:
                return jsonify({'error': f'Erro ao consultar o serviço de CEP: {str(e)}'}), 500

        # Atualiza os campos permitidos
        user.nome = data.get('nome', user.nome)
        user.email = data.get('email', user.email)
        user.setor = data.get('setor', user.setor)
        user.funcao = data.get('funcao', user.funcao)
        user.telefone = data.get('telefone', user.telefone)
        user.especialidade = data.get('especialidade', user.especialidade)
        user.registro_categoria = data.get('registro_categoria', user.registro_categoria)
        user.tipo_acesso = data.get('tipo_acesso', user.tipo_acesso)
        user.tipo_contratacao = data.get('tipo_contratacao', user.tipo_contratacao)
        user.status = data.get('status', user.status)

        # Só atualizar o endereço se não foi alterado pelo CEP
        if 'endereco' in data and not new_cep:
            user.endereco = data.get('endereco')

        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso', 'user': user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar usuário: {str(e)}'}), 500

@user_routes.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    Exclui logicamente um usuário (soft delete).
    """
    try:
        user = User.query.get(id)
        if not user:
            raise NotFound('Usuário não encontrado')

        # Marca o usuário como inativo
        user.status = 'Inativo'
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao excluir usuário: {str(e)}'}), 500

@user_routes.route('/usuarios/visualizar/<int:id>', methods=['GET'])
def visualizar_usuario(id):
    """
    Retorna os detalhes de um usuário específico pelo ID, excluindo o campo password_hash.
    """
    try:
        user = User.query.get(id)
        if not user:
            raise NotFound('Usuário não encontrado')

        # Converte o usuário para dicionário e remove o campo password_hash
        user_data = user.to_dict()
        user_data.pop('password_hash', None)

        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar usuário: {str(e)}'}), 500

# Registrar o Blueprint no aplicativo
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)