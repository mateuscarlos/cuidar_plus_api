from flask import Blueprint, request, jsonify
from db import db
from models.convenio import Convenio
from models.plano import Plano

convenios_routes = Blueprint('convenios_routes', __name__)

# CONVÊNIOS

@convenios_routes.route('/convenios/listar', methods=['GET'])
def listar_convenios():
    """Listar todos os convênios"""
    try:
        convenios = Convenio.query.all()
        resultado = [convenio.to_dict() for convenio in convenios]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/convenios/<int:id>', methods=['GET'])
def obter_convenio(id):
    """Obter um convênio pelo ID"""
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        return jsonify(convenio.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/convenios/criar', methods=['POST'])
def criar_convenio():
    """Criar um novo convênio"""
    try:
        data = request.get_json()
        
        novo_convenio = Convenio(nome=data.get('nome'))
        
        db.session.add(novo_convenio)
        db.session.commit()
        
        return jsonify(novo_convenio.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/planos/convenios/<int:id>', methods=['GET'])
def obter_planos_convenio(id):
    """Obter planos de um convênio específico"""
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        planos = Plano.query.filter_by(convenio_id=id).all()
        resultado = [p.to_dict() for p in planos]
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/convenios/<int:id>/planos', methods=['POST'])
def criar_plano(id):
    """Criar um novo plano para um convênio"""
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        data = request.get_json()
        
        novo_plano = Plano(
            nome=data.get('nome'),
            convenio_id=id
        )
        
        db.session.add(novo_plano)
        db.session.commit()
        
        return jsonify(novo_plano.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# PLANOS

@convenios_routes.route('/planos', methods=['GET'])
def listar_planos():
    """Listar todos os planos"""
    try:
        planos = Plano.query.all()
        resultado = [plano.to_dict() for plano in planos]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/planos/<int:id>', methods=['GET'])
def obter_plano(id):
    """Obter um plano pelo ID"""
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        return jsonify(plano.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/planos/<int:id>', methods=['PUT'])
def atualizar_plano(id):
    """Atualizar um plano existente"""
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        data = request.get_json()
        plano.nome = data.get('nome', plano.nome)
        
        db.session.commit()
        
        return jsonify(plano.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/planos/<int:id>/status', methods=['PATCH'])
def alterar_status_plano(id):
    """Alterar status de um plano (ativar/desativar)"""
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        data = request.get_json()
        plano.ativo = data.get('ativo', plano.ativo)
        
        db.session.commit()
        
        return jsonify(plano.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500