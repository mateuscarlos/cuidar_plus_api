from flask import Blueprint, request, jsonify
from db import db
from models.convenio import Convenio
from models.plano import Plano

convenios_routes = Blueprint('convenios_routes', __name__)

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

@convenios_routes.route('/convenios/<int:id>/planos', methods=['GET'])
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

@convenios_routes.route('/planos', methods=['GET'])
def obter_todos_planos():
    """Obter todos os planos"""
    try:
        planos = Plano.query.all()
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