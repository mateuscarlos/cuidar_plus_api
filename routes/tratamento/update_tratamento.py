from flask import request, jsonify
from models.tratamento import Tratamento
from db import db
from utils import sanitize_input, convert_ddmmyyyy_to_db_format, get_local_time, get_user_timezone
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime, timezone

def update_tratamento(tratamento_id):
    try:
        tratamento = Tratamento.query.get(tratamento_id)
        if not tratamento:
            raise NotFound("Tratamento não encontrado")
        
        data = request.get_json()
        
        # Campos que podem ser atualizados
        if 'medicamento' in data:
            tratamento.medicamento = sanitize_input(str(data['medicamento']), 100)
        
        if 'posologia' in data:
            tratamento.posologia = sanitize_input(str(data['posologia']), 200)
        
        if 'frequencia' in data:
            tratamento.frequencia = sanitize_input(str(data['frequencia']), 50)
        
        if 'duracao' in data:
            tratamento.duracao = sanitize_input(str(data['duracao']), 50)
        
        if 'data_inicio' in data:
            tratamento.data_inicio = convert_ddmmyyyy_to_db_format(data['data_inicio'])
        
        if 'data_fim' in data:
            tratamento.data_fim = convert_ddmmyyyy_to_db_format(data['data_fim']) if data['data_fim'] else None
        
        if 'observacoes' in data:
            tratamento.observacoes = sanitize_input(str(data.get('observacoes', '')), 500) if data.get('observacoes') else None
        
        if 'status' in data:
            tratamento.status = sanitize_input(str(data['status']), 20)
        
        tratamento.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)
        
        return jsonify({
            'message': 'Tratamento atualizado com sucesso',
            'id': tratamento.id,
            'updated_at': get_local_time(tratamento.updated_at, user_timezone).isoformat()
        }), 200
        
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao atualizar tratamento', 'error': str(e)}), 500