from flask import request, jsonify
from models.convenio import Convenio
from models.plano import Plano
from db import db
from utils import sanitize_input
from werkzeug.exceptions import NotFound, BadRequest
from datetime import datetime

def create_plano(convenio_id):
    """
    Cria um novo plano para um convênio específico
    ---
    tags:
      - Convênios
    parameters:
      - in: path
        name: convenio_id
        type: integer
        required: true
        description: ID do convênio
      - in: body
        name: body
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              description: Nome do plano
            codigo:
              type: string
              description: Código do plano
            tipo_acomodacao:
              type: string
              description: Tipo de acomodação do plano
            ativo:
              type: boolean
              description: Status do plano
    responses:
      201:
        description: Plano criado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Convênio não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        # Verificar se o convênio existe
        convenio = Convenio.query.get(convenio_id)
        if not convenio:
            raise NotFound(f"Convênio com ID {convenio_id} não encontrado")
        
        data = request.get_json()
        
        # Verificar campos obrigatórios
        if not data.get('nome'):
            raise BadRequest("O nome do plano é obrigatório")
        
        # Criar o plano
        plano = Plano(
            convenio_id=convenio_id,
            nome=sanitize_input(data['nome'], 100),
            codigo=sanitize_input(data.get('codigo'), 20) if data.get('codigo') else None,
            tipo_acomodacao=sanitize_input(data.get('tipo_acomodacao'), 50) if data.get('tipo_acomodacao') else None,
            ativo=data.get('ativo', True),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(plano)
        db.session.commit()
        
        return jsonify({
            'message': 'Plano criado com sucesso',
            'id': plano.id,
            'plano': plano.to_dict()
        }), 201
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Erro ao criar plano',
            'error': str(e)
        }), 500