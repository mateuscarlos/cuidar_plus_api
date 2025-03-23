from flask import request, jsonify
from models.pacientes import Paciente
from db import db
from utils import validate_cpf, sanitize_input, get_local_time, get_user_timezone, convert_utc_to_db_format, convert_ddmmyyyy_to_db_format
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime, timezone

def atualizar_paciente(paciente_id):
    try:
        # Buscar paciente pelo ID
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            raise NotFound("Paciente não encontrado")

        data = request.get_json()
        
        # Validar CPF se ele for alterado
        if data.get('cpf') and data.get('cpf') != paciente.cpf:
            if not validate_cpf(data.get('cpf')):
                raise BadRequest("CPF inválido")
                
            # Verificar se o novo CPF já existe em outro paciente
            existing_paciente = Paciente.query.filter_by(cpf=data.get('cpf')).first()
            if existing_paciente and existing_paciente.id != int(paciente_id):
                raise BadRequest("CPF já cadastrado para outro paciente")

        # Incluir todos os campos do modelo de paciente
        update_fields = {
            'nome_completo': sanitize_input(data.get('nome_completo'), 100) if 'nome_completo' in data else None,
            'cpf': sanitize_input(data.get('cpf'), 11) if 'cpf' in data else None,
            'operadora': sanitize_input(data.get('operadora'), 50) if 'operadora' in data else None,
            'identificador_prestadora': sanitize_input(data.get('identificador_prestadora'), 50) if 'identificador_prestadora' in data else None,
            'acomodacao': sanitize_input(data.get('acomodacao'), 50) if 'acomodacao' in data else None,
            'telefone': sanitize_input(data.get('telefone'), 15) if 'telefone' in data else None,
            'alergias': sanitize_input(data.get('alergias'), 200) if 'alergias' in data else None,
            'cid_primario': sanitize_input(data.get('cid_primario'), 10) if 'cid_primario' in data else None,
            'cid_secundario': sanitize_input(data.get('cid_secundario'), 10) if 'cid_secundario' in data else None,
            'data_nascimento': convert_ddmmyyyy_to_db_format(data.get('data_nascimento')) if 'data_nascimento' in data else None,
            'rua': sanitize_input(data.get('rua'), 100) if 'rua' in data else None,
            'numero': sanitize_input(data.get('numero'), 10) if 'numero' in data else None,
            'complemento': sanitize_input(data.get('complemento'), 50) if 'complemento' in data else None,
            'cep': sanitize_input(data.get('cep'), 8) if 'cep' in data else None,
            'bairro': sanitize_input(data.get('bairro'), 50) if 'bairro' in data else None,
            'cidade': sanitize_input(data.get('cidade'), 50) if 'cidade' in data else None,
            'estado': sanitize_input(data.get('estado'), 2) if 'estado' in data else None,
            'status': sanitize_input(data.get('status'), 20) if 'status' in data else None,
            'email': sanitize_input(data.get('email'), 100) if 'email' in data else None,
            'telefone_emergencia': sanitize_input(data.get('telefone_emergencia'), 15) if 'telefone_emergencia' in data else None,
            'contato_emergencia': sanitize_input(data.get('contato_emergencia'), 100) if 'contato_emergencia' in data else None,
            'case_responsavel': sanitize_input(data.get('case_responsavel'), 100) if 'case_responsavel' in data else None,
            'medico_responsavel': sanitize_input(data.get('medico_responsavel'), 100) if 'medico_responsavel' in data else None,
            'updated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        }

        # Atualizar apenas os campos que foram enviados na requisição
        for key, value in update_fields.items():
            if value is not None:
                setattr(paciente, key, value)
        
        db.session.commit()
        
        # Obter fuso horário do usuário
        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)
        
        # Retornar mensagem de sucesso e o paciente atualizado
        return jsonify({
            'message': 'Paciente atualizado com sucesso!', 
            'updated_at': get_local_time(paciente.updated_at, user_timezone).isoformat(),
            'paciente': paciente.to_dict()
        }), 200

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500