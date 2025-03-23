from flask import jsonify, request
from models.tratamento import Tratamento
from models.pacientes import Paciente
from utils import get_local_time, get_user_timezone
from werkzeug.exceptions import NotFound

def get_tratamentos_by_paciente(paciente_id):
    """
    Recupera todos os tratamentos de um paciente específico
    """
    try:
        # Verificar se o paciente existe
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            raise NotFound(f"Paciente com ID {paciente_id} não encontrado")
            
        tratamentos = Tratamento.query.filter_by(paciente_id=paciente_id).all()
        
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
        
        return jsonify({
            'paciente_id': paciente_id,
            'paciente_nome': paciente.nome,
            'tratamentos': tratamentos_list
        }), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': 'Erro ao recuperar tratamentos do paciente', 'error': str(e)}), 500