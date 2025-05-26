from flask import Blueprint, request, jsonify
from models.setor import Setor
from db import db

setores_bp = Blueprint('setores', __name__)

@setores_bp.route('/setores', methods=['GET'])
def get_setores():
    try:
        setores = Setor.query.all()
        return jsonify([setor.to_dict() for setor in setores]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@setores_bp.route('/setores/<int:setor_id>', methods=['GET'])
def get_setor(setor_id):
    try:
        setor = Setor.query.get_or_404(setor_id)
        return jsonify(setor.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@setores_bp.route('/setores', methods=['POST'])
def create_setor():
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('nome'):
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        setor = Setor(
            nome=data['nome'],
            descricao=data.get('descricao'),
            status=data.get('status', True)
        )
        
        db.session.add(setor)
        db.session.commit()
        
        return jsonify(setor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@setores_bp.route('/setores/<int:setor_id>', methods=['PUT'])
def update_setor(setor_id):
    try:
        setor = Setor.query.get_or_404(setor_id)
        data = request.get_json()
        
        # Validações
        if not data.get('nome'):
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        setor.nome = data['nome']
        setor.descricao = data.get('descricao')
        setor.status = data.get('status', setor.status)
        
        db.session.commit()
        
        return jsonify(setor.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@setores_bp.route('/setores/<int:setor_id>', methods=['DELETE'])
def delete_setor(setor_id):
    try:
        setor = Setor.query.get_or_404(setor_id)
        
        # Soft delete - apenas marca como inativo
        setor.status = False
        db.session.commit()
        
        return jsonify({'message': 'Setor desativado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@setores_bp.route('/setores/ativos', methods=['GET'])
def get_setores_ativos():
    try:
        setores = Setor.get_setores_ativos()
        return jsonify([setor.to_dict() for setor in setores]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500