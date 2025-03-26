from flask import jsonify
from models.convenio import Convenio
from models.plano import Plano
from werkzeug.exceptions import NotFound

def get_planos_by_convenio(convenio_id):
    """
    Recupera todos os planos de um convênio específico
    ---
    tags:
      - Convênios
    parameters:
      - in: path
        name: convenio_id
        type: integer
        required: true
        description: ID do convênio
    responses:
      200:
        description: Lista dos planos do convênio
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
        
        # Recuperar os planos do convênio
        planos = Plano.query.filter_by(convenio_id=convenio_id).all()
        
        planos_list = [plano.to_dict() for plano in planos]
        
        return jsonify({
            'convenio': convenio.to_dict(),
            'total': len(planos_list),
            'planos': planos_list
        }), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({
            'message': 'Erro ao recuperar planos do convênio',
            'error': str(e)
        }), 500

def get_plano_by_id(convenio_id, plano_id):
    """
    Recupera um plano específico de um convênio
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
    responses:
      200:
        description: Detalhes do plano
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
        
        return jsonify({
            'plano': plano.to_dict(),
            'convenio': convenio.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({
            'message': 'Erro ao recuperar detalhes do plano',
            'error': str(e)
        }), 500