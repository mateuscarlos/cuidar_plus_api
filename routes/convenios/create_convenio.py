from flask import request, jsonify
from models.convenio import Convenio
from db import db
from utils import sanitize_input
from werkzeug.exceptions import BadRequest
from datetime import datetime

def create_convenio():
    """
    Cria um novo convênio
    ---
    tags:
      - Convênios
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              description: Nome do convênio
            codigo:
              type: string
              description: Código do convênio
            tipo:
              type: string
              description: Tipo do convênio
            ativo:
              type: boolean
              description: Status do convênio
    responses:
      201:
        description: Convênio criado com sucesso
      400:
        description: Dados inválidos
      500:
        description: Erro interno no servidor
    """
    try:
        data = request.get_json()
        
        # Verificar campos obrigatórios
        if not data.get('nome'):
            raise BadRequest("O nome do convênio é obrigatório")
        
        # Criar o convênio
        convenio = Convenio(
            nome=sanitize_input(data['nome'], 100),
            codigo=sanitize_input(data.get('codigo'), 20) if data.get('codigo') else None,
            tipo=sanitize_input(data.get('tipo'), 50) if data.get('tipo') else None,
            ativo=data.get('ativo', True),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(convenio)
        db.session.commit()
        
        return jsonify({
            'message': 'Convênio criado com sucesso',
            'id': convenio.id,
            'convenio': convenio.to_dict()
        }), 201
        
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Erro ao criar convênio',
            'error': str(e)
        }), 500