from flask import Blueprint, jsonify
from models.user import User
from werkzeug.exceptions import InternalServerError

get_all_users_bp = Blueprint('get_all_users', __name__)

@get_all_users_bp.route('/api/exibe_usuarios', methods=['GET'])
def exibe_usuarios():
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

        # Retorna a lista de usuários sem senha
        usuarios_sem_senha = [
            {
                'id': usuario.id,
                'email': usuario.email,
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
                'telefone': usuario.telefone,
                'data_admissao': usuario.data_admissao,
                'status': usuario.status,
                'tipo_acesso': usuario.tipo_acesso
            }
            for usuario in usuarios
        ]
        return jsonify({'usuarios': usuarios_sem_senha}), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao recuperar usuários', 'error': str(e)}), 500