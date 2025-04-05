from flask import Blueprint, request, jsonify
from models.pacientes import Paciente
from db import db
from services.datetime_service import DateTimeService
from utils import sanitize_input
from datetime import datetime

paciente_bp = Blueprint('paciente', __name__)

@paciente_bp.route('/pacientes', methods=['POST'])
def criar_paciente():
    try:
        dados = request.get_json()
        
        # Criar paciente usando o método from_json que já processa as datas
        paciente = Paciente.from_json(dados)
        
        # Adicionar ao banco de dados
        db.session.add(paciente)
        db.session.commit()
        
        # Converter para JSON com datas no formato brasileiro
        return jsonify({
            'message': 'Paciente cadastrado com sucesso',
            'paciente': paciente.to_json()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao cadastrar paciente: {str(e)}'}), 500

@paciente_bp.route('/pacientes/<int:id>', methods=['PUT'])
def atualizar_paciente(id):
    try:
        dados = request.get_json()
        paciente = Paciente.query.get(id)
        
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        # Processar dados para garantir formato correto para o banco de dados
        processed_data = DateTimeService.process_form_data(dados)
        
        # Atualizar campos
        if 'nome' in processed_data:
            paciente.nome = sanitize_input(processed_data['nome'])
        if 'cpf' in processed_data:
            paciente.cpf = sanitize_input(processed_data['cpf'])
        if 'data_nascimento' in processed_data:
            paciente.data_nascimento = processed_data['data_nascimento']
        
        # ... outros campos
        
        paciente.updated_at = datetime.now()
        db.session.commit()
        
        return jsonify({
            'message': 'Paciente atualizado com sucesso',
            'paciente': paciente.to_json()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar paciente: {str(e)}'}), 500

@paciente_bp.route('/pacientes/<int:id>', methods=['GET'])
def obter_paciente(id):
    try:
        paciente = Paciente.query.get(id)
        
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        # Converter para JSON com datas no formato brasileiro
        return jsonify(paciente.to_json()), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao obter paciente: {str(e)}'}), 500

@paciente_bp.route('/pacientes', methods=['GET'])
def listar_pacientes():
    try:
        pacientes = Paciente.query.all()
        # Converter cada paciente para JSON com datas no formato brasileiro
        return jsonify([paciente.to_json() for paciente in pacientes]), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao listar pacientes: {str(e)}'}), 500