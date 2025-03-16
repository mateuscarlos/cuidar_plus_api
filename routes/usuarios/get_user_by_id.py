from flask import Flask, Blueprint, request, jsonify
from models.user import User
from db import db
from flasgger import Swagger
import re
import bleach
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from utils import validate_cpf, sanitize_input

get_user_by_id_bp = Blueprint('get_user_by_id', __name__)

@get_user_by_id_bp.route('/api/usuario/<int:id>', methods=['GET'])
def get_usuario_by_id(id):
    """
    Obtém os dados de um usuário pelo ID
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Dados do usuário
      400:
        description: ID inválido
      404:
        description: Usuário não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        if not str(id).isdigit():
            raise BadRequest("ID inválido")
            
        usuario = User.query.filter_by(id=id).first()
        if not usuario:
            raise NotFound("Usuário não encontrado")

        return jsonify({
            'usuario': {
                'id': usuario.id,
                'nome': usuario.nome,
                'cpf': usuario.cpf,
                'rua': usuario.rua,
                'numero': usuario.numero,
                'complemento': usuario.complemento,
                'cep': usuario.cep,
                'bairro': usuario.bairro,
                'cidade': usuario.cidade,
                'estado': usuario.estado,
                'setor': usuario.setor,
                'funcao': usuario.funcao,
                'especialidade': usuario.especialidade,
                'registro_categoria': usuario.registro_categoria,
                'email': usuario.email,
                'telefone': usuario.telefone,
                'data_admissao': usuario.data_admissao,
                'status': usuario.status,
                'tipo_acesso': usuario.tipo_acesso
            }
        }), 200

    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500

