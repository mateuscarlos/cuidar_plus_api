from flask import jsonify
from models.tratamento import Tratamento
from db import db
from werkzeug.exceptions import NotFound

def delete_tratamento(tratamento_id):
    try:
        tratamento = Tratamento.query.get(tratamento_id)
        if not tratamento:
            raise NotFound("Tratamento não encontrado")
        
        db.session.delete(tratamento)
        db.session.commit()
        
        return jsonify({
            'message': 'Tratamento excluído com sucesso',
            'id': tratamento_id
        }), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao excluir tratamento', 'error': str(e)}), 500