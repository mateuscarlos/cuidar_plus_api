from flask import Blueprint, jsonify
from models.user import User
from werkzeug.exceptions import InternalServerError

get_all_users_bp = Blueprint('get_all_users', __name__)

@get_all_users_bp.route('/api/exibe_usuarios', methods=['GET'])
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