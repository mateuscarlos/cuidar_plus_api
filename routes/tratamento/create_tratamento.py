from flask import request, jsonify
from models.tratamento import Tratamento
from models.pacientes import Paciente
from db import db
from utils import sanitize_input, convert_ddmmyyyy_to_db_format, get_local_time, get_user_timezone
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime, timezone

def create_tratamento():
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = ['paciente_id', 'medicamento', 'posologia', 'frequencia', 'data_inicio']
        for field in required_fields:
            if field not in data or not data[field]:
                raise BadRequest(f"Campo obrigatório: {field}")
        
        # Verificar se o paciente existe
        paciente_id = data['paciente_id']
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            raise NotFound(f"Paciente com ID {paciente_id} não encontrado")
        
        # Criar novo tratamento
        novo_tratamento = Tratamento(
            paciente_id=paciente_id,
            medicamento=sanitize_input(str(data['medicamento']), 100),
            posologia=sanitize_input(str(data['posologia']), 200),
            frequencia=sanitize_input(str(data['frequencia']), 50),
            duracao=sanitize_input(str(data['duracao']), 50) if 'duracao' in data and data['duracao'] else None,
            data_inicio=convert_ddmmyyyy_to_db_format(data['data_inicio']),
            data_fim=convert_ddmmyyyy_to_db_format(data['data_fim']) if 'data_fim' in data and data['data_fim'] else None,
            observacoes=sanitize_input(str(data.get('observacoes', '')), 500) if data.get('observacoes') else None,
            status=sanitize_input(str(data.get('status', 'Ativo')), 20),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        db.session.add(novo_tratamento)
        db.session.commit()
        
        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)
        
        return jsonify({
            'message': 'Tratamento criado com sucesso',
            'id': novo_tratamento.id,
            'created_at': get_local_time(novo_tratamento.created_at, user_timezone).isoformat()
        }), 201
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar tratamento', 'error': str(e)}), 500