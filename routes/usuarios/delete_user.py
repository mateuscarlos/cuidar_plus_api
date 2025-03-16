from flask import Flask, Blueprint, request, jsonify
from models.user import User
from db import db
from flasgger import Swagger
import re
import bleach
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from utils import validate_cpf, sanitize_input

delete_user_bp = Blueprint('delete_user', __name__)

@delete_user_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Exclui um usuário existente
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
        description: Usuário excluído com sucesso
      400:
        description: ID inválido
      404:
        description: Usuário não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        if not id.isdigit():
            raise BadRequest("ID inválido")
            
        usuario = User.query.filter_by(id=id).first()
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
    

   