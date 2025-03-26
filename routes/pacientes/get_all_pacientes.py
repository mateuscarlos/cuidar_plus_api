from flask import request, jsonify
from models.pacientes import Paciente
from utils import get_local_time, get_user_timezone

def get_all_pacientes():
    try:
        pacientes = Paciente.query.all()
        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)
        
        return jsonify({
            'pacientes': [{
                'id': p.id,
                'nome_completo': p.nome_completo,
                'cpf': p.cpf,
                'connvenio_id': p.convenio_id,
                'cid_primario': p.cid_primario,
                'numero_carteirinha': p.numero_carteirinha,
                'acomodacao': p.acomodacao,
                'telefone': p.telefone,
                'alergias': p.alergias,
                'cid_secundario': p.cid_secundario,
                'data_nascimento': p.data_nascimento,
                'rua': p.rua,
                'numero': p.numero,
                'complemento': p.complemento,
                'cep': p.cep,
                'bairro': p.bairro,
                'cidade': p.cidade,
                'estado': p.estado,
                'status': p.status,
                'created_at': p.created_at.isoformat(),
                'updated_at': get_local_time(p.updated_at, user_timezone).isoformat()
            } for p in pacientes]
        }), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao recuperar pacientes', 'error': str(e)}), 500