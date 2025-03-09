from flask import request, jsonify
from models.pacientes import Paciente
from db import db
from utils import validate_cpf, sanitize_input, get_local_time, get_user_timezone
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime, timezone

def atualizar_paciente(cpf):
    try:
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        paciente = Paciente.query.filter_by(cpf=cpf).first()
        if not paciente:
            raise NotFound("Paciente não encontrado")

        data = request.get_json()
        update_fields = {
            'nome_completo': sanitize_input(data.get('nome_completo'), 100) if data.get('nome_completo') else None,
            'operadora': sanitize_input(data.get('operadora'), 50) if data.get('operadora') else None,
            'cid_primario': sanitize_input(data.get('cid_primario'), 10) if data.get('cid_primario') else None,
            'identificador_prestadora': sanitize_input(data.get('identificador_prestadora'), 50) if data.get('identificador_prestadora') else None,
            'acomodacao': sanitize_input(data.get('acomodacao'), 50) if data.get('acomodacao') else None,
            'telefone': sanitize_input(data.get('telefone'), 15) if data.get('telefone') else None,
            'alergias': sanitize_input(data.get('alergias'), 255) if data.get('alergias') else None,
            'cid_secundario': sanitize_input(data.get('cid_secundario'), 10) if data.get('cid_secundario') else None,
            'data_nascimento': sanitize_input(data.get('data_nascimento'), 10) if data.get('data_nascimento') else None,
            'rua': sanitize_input(data.get('rua'), 100) if data.get('rua') else None,
            'numero': sanitize_input(data.get('numero'), 10) if data.get('numero') else None,
            'complemento': sanitize_input(data.get('complemento'), 50) if data.get('complemento') else None,
            'cep': sanitize_input(data.get('cep'), 8) if data.get('cep') else None,
            'bairro': sanitize_input(data.get('bairro'), 50) if data.get('bairro') else None,
            'cidade': sanitize_input(data.get('cidade'), 50) if data.get('cidade') else None,
            'estado': sanitize_input(data.get('estado'), 2) if data.get('estado') else None,
            'status': sanitize_input(data.get('status'), 20) if data.get('status') else None,
            'updated_at': datetime.now(timezone.utc)
        }

        for key, value in update_fields.items():
            if value is not None:
                setattr(paciente, key, value)
        
        db.session.commit()
        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)
        return jsonify({'message': 'Paciente atualizado com sucesso!', 'updated_at': get_local_time(paciente.updated_at, user_timezone).isoformat()}), 200

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500