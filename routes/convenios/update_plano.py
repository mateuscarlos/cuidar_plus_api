from flask import request, jsonify
from models.plano import Plano
from models.convenio import Convenio
from db import db
from utils import sanitize_input
from werkzeug.exceptions import NotFound, BadRequest
from datetime import datetime

def update_plano(convenio_id, plano_id):
    """
    Atualiza um plano existente de um convênio
    ---
    tags:
      - Convênios
    parameters:
      - in: path
        name: convenio_id
        type: integer
        required: true
        description: ID do convênio
      - in: path
        name: plano_id
        type: integer
        required: true
        description: ID do plano
      - in: body
        name: body
        schema:
          type: object
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
      200:
        description: Plano atualizado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Convênio ou plano não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        # Verificar se o convênio existe
        convenio = Convenio.query.get(convenio_id)
        if not convenio:
            raise NotFound(f"Convênio com ID {convenio_id} não encontrado")
        
        # Verificar se o plano existe e pertence ao convênio
        plano = Plano.query.filter_by(id=plano_id, convenio_id=convenio_id).first()
        if not plano:
            raise NotFound(f"Plano com ID {plano_id} não encontrado para o convênio especificado")
        
        data = request.get_json()
        
        # Atualiza apenas os campos enviados na requisição
        if 'nome' in data:
            plano.nome = sanitize_input(data['nome'], 100)
        
        if 'codigo' in data:
            plano.codigo = sanitize_input(data['codigo'], 20) if data['codigo'] else None
        
        if 'tipo_acomodacao' in data:
            plano.tipo_acomodacao = sanitize_input(data['tipo_acomodacao'], 50) if data['tipo_acomodacao'] else None
        
        if 'ativo' in data:
            plano.ativo = data['ativo']
        
        plano.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Plano atualizado com sucesso',
            'plano': plano.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Erro ao atualizar plano',
            'error': str(e)
        }), 500