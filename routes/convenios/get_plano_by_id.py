from flask import jsonify
from models.plano import Plano
from models.convenio import Convenio
from werkzeug.exceptions import NotFound

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