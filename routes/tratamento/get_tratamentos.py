from flask import jsonify, request
from models.tratamento import Tratamento
from utils import get_local_time, get_user_timezone

def get_tratamentos():
    """
    Recupera todos os tratamentos
    """
    try:
        tratamentos = Tratamento.query.all()
        
        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)
        
        tratamentos_list = []
        for tratamento in tratamentos:
            tratamento_dict = tratamento.to_dict()
            
            # Converter horários para timezone do usuário
            if tratamento.created_at:
                tratamento_dict['created_at'] = get_local_time(tratamento.created_at, user_timezone).isoformat()
            if tratamento.updated_at:
                tratamento_dict['updated_at'] = get_local_time(tratamento.updated_at, user_timezone).isoformat()
            
            tratamentos_list.append(tratamento_dict)
        
        return jsonify({'tratamentos': tratamentos_list}), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro ao recuperar tratamentos', 'error': str(e)}), 500