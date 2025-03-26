from flask import request, jsonify
from models.convenio import Convenio
from db import db
from utils import sanitize_input
from werkzeug.exceptions import NotFound, BadRequest
from datetime import datetime

def update_convenio(convenio_id):
    """
    Atualiza um convênio existente
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
      200:
        description: Convênio atualizado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Convênio não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        convenio = Convenio.query.get(convenio_id)
        
        if not convenio:
            raise NotFound(f"Convênio com ID {convenio_id} não encontrado")
        
        data = request.get_json()
        
        # Atualiza apenas os campos enviados na requisição
        if 'nome' in data:
            convenio.nome = sanitize_input(data['nome'], 100)
        
        if 'codigo' in data:
            convenio.codigo = sanitize_input(data['codigo'], 20) if data['codigo'] else None
        
        if 'tipo' in data:
            convenio.tipo = sanitize_input(data['tipo'], 50) if data['tipo'] else None
        
        if 'ativo' in data:
            convenio.ativo = data['ativo']
        
        convenio.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Convênio atualizado com sucesso',
            'convenio': convenio.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Erro ao atualizar convênio',
            'error': str(e)
        }), 500