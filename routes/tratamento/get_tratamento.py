from flask import request, jsonify
from models.tratamento import Tratamento
from utils import get_local_time, get_user_timezone
from werkzeug.exceptions import NotFound

def get_tratamento(tratamento_id):
    try:
        tratamento = Tratamento.query.get(tratamento_id)
        
        if not tratamento:
            raise NotFound("Tratamento não encontrado")
        
        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)
        
        tratamento_dict = tratamento.to_dict()
        
        # Converter horários para timezone do usuário
        if tratamento.created_at:
            tratamento_dict['created_at'] = get_local_time(tratamento.created_at, user_timezone).isoformat()
        if tratamento.updated_at:
            tratamento_dict['updated_at'] = get_local_time(tratamento.updated_at, user_timezone).isoformat()
        
        return jsonify({'tratamento': tratamento_dict}), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': 'Erro ao recuperar tratamento', 'error': str(e)}), 500