from flask import request, jsonify
from models.pacientes import Paciente
from db import db

def get_paciente_by_id_from_db(id):
    paciente = Paciente.query.get(id)
    if paciente:
        return {
            'id': paciente.id,
            'nome_completo': paciente.nome_completo,
            'cpf': paciente.cpf,
            'convenio_id': paciente.convenio_id,
            'numero_carteirinha': paciente.numero_carteirinha,
            'acomodacao': paciente.acomodacao,
            'telefone': paciente.telefone,
            'alergias': paciente.alergias,
            'cid_primario': paciente.cid_primario,
            'cid_secundario': paciente.cid_secundario,
            'data_nascimento': paciente.data_nascimento.strftime('%Y-%m-%d'),
            'rua': paciente.rua,
            'numero': paciente.numero,
            'complemento': paciente.complemento,
            'cep': paciente.cep,
            'bairro': paciente.bairro,
            'cidade': paciente.cidade,
            'estado': paciente.estado,
            'status': paciente.status,
            'created_at': paciente.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': paciente.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    return None

def get_paciente_by_id(id):
    paciente = get_paciente_by_id_from_db(id)
    if paciente:
        return jsonify({'paciente': paciente}), 200
    else:
        return jsonify({'error': 'Paciente not found'}), 404