from flask import Blueprint, request, jsonify, abort
from infrastructure.database.db_config import db
from models.acompanhamento import Acompanhamento
from models.pacientes import Paciente
import json
from datetime import datetime
from infrastructure.utils.validators import convert_ddmmyyyy_to_db_format, convert_utc_to_db_format

acompanhamentos_routes = Blueprint('acompanhamentos', __name__)

@acompanhamentos_routes.route('/acompanhamentos', methods=['POST'])
def criar_acompanhamento():
    """Criar um novo acompanhamento"""
    try:
        data = request.get_json()
        
        # Verificar se o paciente existe
        paciente = Paciente.query.get(data.get('paciente_id'))
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        # Converter data_hora_atendimento para formato de data
        data_hora_str = data.get('data_hora_atendimento')
        if data_hora_str:
            try:
                data_hora = datetime.strptime(data_hora_str, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                try:
                    data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return jsonify({'error': 'Formato de data inválido'}), 400
        else:
            data_hora = datetime.now()
            
        # Criar o acompanhamento básico
        acompanhamento = Acompanhamento(
            paciente_id=data.get('paciente_id'),
            data_hora=data_hora,
            tipo_atendimento=data.get('tipo_atendimento'),
            motivo_atendimento=data.get('motivo_atendimento'),
            descricao=data.get('descricao_motivo')
        )
        
        # Processar dados JSON para estruturas complexas
        if 'sinais_vitais' in data:
            acompanhamento.sinais_vitais = data.get('sinais_vitais')
            
        if 'avaliacao_feridas' in data:
            acompanhamento.avaliacao_feridas = data.get('avaliacao_feridas')
            
        if 'avaliacao_dispositivos' in data:
            acompanhamento.avaliacao_dispositivos = data.get('avaliacao_dispositivos')
            
        if 'intervencoes' in data:
            acompanhamento.intervencoes = data.get('intervencoes')
            
        if 'plano_acao' in data:
            acompanhamento.plano_acao = data.get('plano_acao')
            
        if 'comunicacao' in data:
            acompanhamento.comunicacao = data.get('comunicacao')
        
        db.session.add(acompanhamento)
        db.session.commit()
        
        return jsonify(acompanhamento.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@acompanhamentos_routes.route('/pacientes/<int:paciente_id>/acompanhamentos', methods=['GET'])
def obter_acompanhamentos_por_paciente(paciente_id):
    """Obter todos os acompanhamentos de um paciente"""
    try:
        # Verificar se o paciente existe
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
            
        acompanhamentos = Acompanhamento.query.filter_by(paciente_id=paciente_id).all()
        result = [a.to_dict() for a in acompanhamentos]
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@acompanhamentos_routes.route('/acompanhamentos/<int:id>', methods=['GET'])
def obter_acompanhamento(id):
    """Obter um acompanhamento específico"""
    try:
        acompanhamento = Acompanhamento.query.get(id)
        if not acompanhamento:
            return jsonify({'error': 'Acompanhamento não encontrado'}), 404
            
        return jsonify(acompanhamento.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@acompanhamentos_routes.route('/acompanhamentos/<int:id>', methods=['PUT'])
def atualizar_acompanhamento(id):
    """Atualizar um acompanhamento existente"""
    try:
        acompanhamento = Acompanhamento.query.get(id)
        if not acompanhamento:
            return jsonify({'error': 'Acompanhamento não encontrado'}), 404
            
        data = request.get_json()
        
        # Atualizar campos básicos
        if 'tipo_atendimento' in data:
            acompanhamento.tipo_atendimento = data['tipo_atendimento']
        if 'motivo_atendimento' in data:
            acompanhamento.motivo_atendimento = data['motivo_atendimento']
        if 'descricao_motivo' in data:
            acompanhamento.descricao = data['descricao_motivo']
            
        # Atualizar campos JSON
        if 'sinais_vitais' in data:
            acompanhamento.sinais_vitais = data['sinais_vitais']
        if 'avaliacao_feridas' in data:
            acompanhamento.avaliacao_feridas = data['avaliacao_feridas']
        if 'avaliacao_dispositivos' in data:
            acompanhamento.avaliacao_dispositivos = data['avaliacao_dispositivos']
        if 'intervencoes' in data:
            acompanhamento.intervencoes = data['intervencoes']
        if 'plano_acao' in data:
            acompanhamento.plano_acao = data['plano_acao']
        if 'comunicacao' in data:
            acompanhamento.comunicacao = data['comunicacao']
            
        db.session.commit()
        
        return jsonify(acompanhamento.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@acompanhamentos_routes.route('/acompanhamentos/<int:id>', methods=['DELETE'])
def excluir_acompanhamento(id):
    """Excluir um acompanhamento"""
    try:
        acompanhamento = Acompanhamento.query.get(id)
        if not acompanhamento:
            return jsonify({'error': 'Acompanhamento não encontrado'}), 404
            
        db.session.delete(acompanhamento)
        db.session.commit()
        
        return jsonify({'message': 'Acompanhamento excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500