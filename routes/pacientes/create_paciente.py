from flask import request, jsonify
from models.pacientes import Paciente
from db import db
from utils import validate_cpf, sanitize_input, get_local_time, get_user_timezone, get_address_from_cep
from werkzeug.exceptions import BadRequest, Conflict
import re
from datetime import datetime, timezone

def create_paciente():
    try:
        data = request.get_json()
        required_fields = ['nome_completo', 'cpf', 'operadora', 'cid_primario', 'cep', 'identificador_prestadora']
        if not all(field in data for field in required_fields):
            raise BadRequest("Campos obrigatórios faltando: nome_completo, cpf, operadora, cid_primario, cep, identificador_prestadora")
        
        cpf = re.sub(r'[^\d]', '', data['cpf'])
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        if Paciente.query.filter_by(cpf=cpf).first():
            raise Conflict("CPF já cadastrado")

        address_data = get_address_from_cep(data['cep'])

        paciente_data = {
            'nome_completo': sanitize_input(str(data['nome_completo']), 100),
            'cpf': cpf,
            'operadora': sanitize_input(str(data['operadora']), 50),
            'cid_primario': sanitize_input(str(data['cid_primario']), 10),
            'identificador_prestadora': sanitize_input(str(data['identificador_prestadora']), 50),
            'rua': address_data.get('logradouro', ''),
            'numero': sanitize_input(str(data.get('numero')), 10) if data.get('numero') else None,
            'complemento': sanitize_input(str(data.get('complemento')), 50) if data.get('complemento') else None,
            'cep': data['cep'],
            'bairro': address_data.get('bairro', ''),
            'cidade': address_data.get('localidade', ''),
            'estado': address_data.get('uf', ''),
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc),
            'status': 'em-avaliacao'
        }

        new_paciente = Paciente(**paciente_data)
        db.session.add(new_paciente)
        db.session.commit()

        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)

        return jsonify({
            'message': 'Paciente criado com sucesso!',
            'id': new_paciente.id,
            'updated_at': get_local_time(new_paciente.updated_at, user_timezone).isoformat()
        }), 201

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except Conflict as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500