from flask import Blueprint, request, jsonify
from models.funcao import Funcao
from models.setor import Setor
from db import db

funcoes_bp = Blueprint('funcoes', __name__)

@funcoes_bp.route('/funcoes', methods=['GET'])
def get_funcoes():
    try:
        funcoes = Funcao.query.all()
        return jsonify([funcao.to_dict() for funcao in funcoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@funcoes_bp.route('/funcoes/<int:funcao_id>', methods=['GET'])
def get_funcao(funcao_id):
    try:
        funcao = Funcao.query.get_or_404(funcao_id)
        return jsonify(funcao.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@funcoes_bp.route('/funcoes/setor/<int:setor_id>', methods=['GET'])
def get_funcoes_por_setor(setor_id):
    try:
        funcoes = Funcao.get_funcoes_por_setor(setor_id)
        return jsonify([funcao.to_dict() for funcao in funcoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@funcoes_bp.route('/funcoes', methods=['POST'])
def create_funcao():
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('nome'):
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        if not data.get('setor_id'):
            return jsonify({'error': 'Setor é obrigatório'}), 400
        
        # Verificar se o setor existe
        setor = Setor.query.get(data['setor_id'])
        if not setor:
            return jsonify({'error': 'Setor não encontrado'}), 404
        
        funcao = Funcao(
            setor_id=data['setor_id'],
            nome=data['nome'],
            descricao=data.get('descricao'),
            nivel_acesso=data.get('nivel_acesso', 1),
            status=data.get('status', True),
            reg_categoria=data.get('reg_categoria')
        )
        
        db.session.add(funcao)
        db.session.commit()
        
        return jsonify(funcao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcoes_bp.route('/funcoes/<int:funcao_id>', methods=['PUT'])
def update_funcao(funcao_id):
    try:
        funcao = Funcao.query.get_or_404(funcao_id)
        data = request.get_json()
        
        # Validações
        if not data.get('nome'):
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        if data.get('setor_id'):
            setor = Setor.query.get(data['setor_id'])
            if not setor:
                return jsonify({'error': 'Setor não encontrado'}), 404
            funcao.setor_id = data['setor_id']
        
        funcao.nome = data['nome']
        funcao.descricao = data.get('descricao')
        funcao.nivel_acesso = data.get('nivel_acesso', funcao.nivel_acesso)
        funcao.status = data.get('status', funcao.status)
        funcao.reg_categoria = data.get('reg_categoria')
        
        db.session.commit()
        
        return jsonify(funcao.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcoes_bp.route('/funcoes/<int:funcao_id>', methods=['DELETE'])
def delete_funcao(funcao_id):
    try:
        funcao = Funcao.query.get_or_404(funcao_id)
        
        # Soft delete - apenas marca como inativo
        funcao.status = False
        db.session.commit()
        
        return jsonify({'message': 'Função desativada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@funcoes_bp.route('/funcoes/ativas', methods=['GET'])
def get_funcoes_ativas():
    try:
        funcoes = Funcao.get_funcoes_ativas()
        return jsonify([funcao.to_dict() for funcao in funcoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500