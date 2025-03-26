from flask import jsonify
from models.convenio import Convenio
from werkzeug.exceptions import NotFound

def get_convenio_by_id(convenio_id):
    """
    Recupera um convênio pelo ID
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
        description: Convênio encontrado
      404:
        description: Convênio não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        convenio = Convenio.query.get(convenio_id)
        
        if not convenio:
            raise NotFound(f"Convênio com ID {convenio_id} não encontrado")
        
        return jsonify({
            'convenio': convenio.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({
            'message': 'Erro ao recuperar convênio',
            'error': str(e)
        }), 500