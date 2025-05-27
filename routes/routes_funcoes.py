from flask import Blueprint, request, jsonify
from models.funcao import Funcao
from db import db

funcao_bp = Blueprint('funcao', __name__)

@funcao_bp.route('/api/funcoes', methods=['GET'])
def get_funcoes():
    try:
        funcoes = Funcao.query.filter_by(status=True).all()
        return jsonify([funcao.to_dict() for funcao in funcoes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@funcao_bp.route('/api/funcoes', methods=['POST'])
def create_funcao():
    try:
        data = request.get_json()
        
        if not data or not data.get('nome'):
            return jsonify({'error': 'O campo nome é obrigatório'}), 400
        
        if not data.get('setor_id'):
            return jsonify({'error': 'O campo setor_id é obrigatório'}), 400
        
        # Verificar se já existe uma função com o mesmo nome no mesmo setor
        existing_funcao = Funcao.query.filter_by(
            nome=data['nome'], 
            setor_id=data['setor_id']
        ).first()
        if existing_funcao:
            return jsonify({'error': 'Função já existe neste setor'}), 400
        
        funcao = Funcao(
            setor_id=data['setor_id'],
            nome=data['nome'],
            descricao=data.get('descricao'),
            nivel_acesso=data.get('nivel_acesso', 1),
            reg_categoria=data.get('reg_categoria'),
            status=data.get('status', True)
        )
        
        db.session.add(funcao)
        db.session.commit()
        
        return jsonify(funcao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcao_bp.route('/api/funcoes/<int:funcao_id>', methods=['PUT'])
def update_funcao(funcao_id):
    try:
        funcao = Funcao.query.get_or_404(funcao_id)
        data = request.get_json()
        
        funcao.nome = data.get('nome', funcao.nome)
        funcao.descricao = data.get('descricao', funcao.descricao)
        funcao.nivel_acesso = data.get('nivel_acesso', funcao.nivel_acesso)
        funcao.reg_categoria = data.get('reg_categoria', funcao.reg_categoria)
        funcao.status = data.get('status', funcao.status)
        
        db.session.commit()
        
        return jsonify(funcao.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcao_bp.route('/api/funcoes/<int:funcao_id>', methods=['DELETE'])
def delete_funcao(funcao_id):
    try:
        funcao = Funcao.query.get_or_404(funcao_id)
        funcao.status = False  # Soft delete
        db.session.commit()
        
        return jsonify({'message': 'Função desativada com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcao_bp.route('/api/funcoes/setor/<int:setor_id>', methods=['GET'])
def get_funcoes_por_setor(setor_id):
    """Retorna todas as funções ativas de um setor específico"""
    try:
        funcoes = Funcao.get_funcoes_por_setor(setor_id)
        return jsonify([funcao.to_dict() for funcao in funcoes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500