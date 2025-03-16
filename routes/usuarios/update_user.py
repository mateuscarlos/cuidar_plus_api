from flask import Flask, Blueprint, request, jsonify
from models.user import User
from db import db
from flasgger import Swagger
import re
import bleach
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from utils import validate_cpf, sanitize_input

update_user_bp = Blueprint('update_user', __name__)

@update_user_bp.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Atualiza um usuário existente
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário
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
