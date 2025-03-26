from flask import jsonify
from models.convenio import Convenio
from models.plano import Plano
from db import db
from werkzeug.exceptions import NotFound

def delete_convenio(convenio_id):
    """
    Exclui um convênio
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
        description: Convênio excluído com sucesso
      404:
        description: Convênio não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        convenio = Convenio.query.get(convenio_id)
        
        if not convenio:
            raise NotFound(f"Convênio com ID {convenio_id} não encontrado")
        
        # Excluir todos os planos associados ao convênio
        Plano.query.filter_by(convenio_id=convenio_id).delete()
        
        # Excluir o convênio
        db.session.delete(convenio)
        db.session.commit()
        
        return jsonify({
            'message': 'Convênio excluído com sucesso'
        }), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Erro ao excluir convênio',
            'error': str(e)
        }), 500