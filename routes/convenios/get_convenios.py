from flask import jsonify
from models.convenio import Convenio
from werkzeug.exceptions import InternalServerError

def get_convenios():
    """
    Recupera todos os convênios cadastrados
    ---
    tags:
      - Convênios
    responses:
      200:
        description: Lista dos convênios
      500:
        description: Erro interno no servidor
    """
    try:
        convenios = Convenio.query.all()
        
        convenios_list = [convenio.to_dict() for convenio in convenios]
        
        return jsonify({
            'total': len(convenios_list),
            'convenios': convenios_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Erro ao recuperar convênios',
            'error': str(e)
        }), 500