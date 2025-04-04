from flask import Blueprint, request, jsonify
from db import db
from models.convenio import Convenio
from models.plano import Plano

# Criação do blueprint unificado
convenio_plano_routes = Blueprint('convenio_plano_routes', __name__)

# ================= ROTAS DE CONVÊNIOS =================

@convenio_plano_routes.route('/convenios/listar', methods=['GET'])
def listar_convenios():
    """Listar todos os convênios ativos"""
    try:
        convenios = Convenio.query.filter_by(ativo=True).all()
        resultado = [{'id': c.id, 'nome': c.nome} for c in convenios]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenio_plano_routes.route('/convenios/<int:id>', methods=['GET'])
def obter_convenio(id):
    """Obter um convênio pelo ID"""
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        return jsonify(convenio.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenio_plano_routes.route('/convenios/criar', methods=['POST'])
def criar_convenio():
    """Criar um novo convênio"""
    try:
        data = request.get_json()
        
        novo_convenio = Convenio(nome=data.get('nome'))
        if 'codigo' in data:
            novo_convenio.codigo = data.get('codigo')
        if 'tipo' in data:
            novo_convenio.tipo = data.get('tipo')
        if 'ativo' in data:
            novo_convenio.ativo = data.get('ativo')
        
        db.session.add(novo_convenio)
        db.session.commit()
        
        return jsonify(novo_convenio.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@convenio_plano_routes.route('/convenios/<int:id>', methods=['PUT'])
def atualizar_convenio(id):
    """Atualizar um convênio existente"""
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        data = request.get_json()
        
        if 'nome' in data:
            convenio.nome = data['nome']
        if 'codigo' in data:
            convenio.codigo = data['codigo']
        if 'tipo' in data:
            convenio.tipo = data['tipo']
        if 'ativo' in data:
            convenio.ativo = data['ativo']
            
        db.session.commit()
        
        return jsonify(convenio.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@convenio_plano_routes.route('/convenios/<int:id>/status', methods=['PATCH'])
def alterar_status_convenio(id):
    """Alterar o status de um convênio (ativar/desativar)"""
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        data = request.get_json()
        if 'ativo' in data:
            convenio.ativo = data['ativo']
            
        db.session.commit()
        
        return jsonify(convenio.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ================= ROTAS DE PLANOS =================

@convenio_plano_routes.route('/planos/listar', methods=['GET'])
def listar_planos():
    """Listar todos os planos ativos"""
    try:
        planos = Plano.query.filter_by(ativo=True).all()
        resultado = []
        
        for plano in planos:
            plano_dict = plano.to_dict()
            # Buscar informações do convênio para cada plano
            convenio = Convenio.query.get(plano.convenio_id)
            if convenio:
                plano_dict['convenio'] = {
                    'id': convenio.id,
                    'nome': convenio.nome
                }
            resultado.append(plano_dict)
            
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenio_plano_routes.route('/planos/convenio/<int:convenio_id>', methods=['GET'])
def listar_planos_por_convenio(convenio_id):
    """Listar planos ativos de um convênio específico"""
    try:
        # Verificar se o convênio existe
        convenio = Convenio.query.get(convenio_id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        # Buscar apenas planos ativos para o convênio especificado
        planos = Plano.query.filter_by(convenio_id=convenio_id, ativo=True).all()
        
        resultado = []
        for plano in planos:
            plano_dict = {
                'id': plano.id, 
                'nome': plano.nome, 
                'codigo': plano.codigo,
                'tipo_acomodacao': plano.tipo_acomodacao,
                'convenio_id': plano.convenio_id,
                'ativo': plano.ativo,
                'convenio': {
                    'id': convenio.id,
                    'nome': convenio.nome
                }
            }
            resultado.append(plano_dict)
            
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenio_plano_routes.route('/planos/<int:id>', methods=['GET'])
def obter_plano(id):
    """Obter um plano pelo ID"""
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        plano_dict = plano.to_dict()
        
        # Adicionar informações do convênio
        convenio = Convenio.query.get(plano.convenio_id)
        if convenio:
            plano_dict['convenio'] = {
                'id': convenio.id,
                'nome': convenio.nome
            }
            
        return jsonify(plano_dict), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenio_plano_routes.route('/planos/criar', methods=['POST'])
def criar_plano():
    """Criar um novo plano"""
    try:
        data = request.get_json()
        
        # Verificar se o convênio existe
        convenio_id = data.get('convenio_id')
        convenio = Convenio.query.get(convenio_id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        novo_plano = Plano(
            nome=data.get('nome'),
            convenio_id=convenio_id,
            ativo=data.get('ativo', True)
        )
        
        if 'codigo' in data:
            novo_plano.codigo = data.get('codigo')
        if 'tipo_acomodacao' in data:
            novo_plano.tipo_acomodacao = data.get('tipo_acomodacao')
        
        db.session.add(novo_plano)
        db.session.commit()
        
        plano_dict = novo_plano.to_dict()
        # Adicionar informações do convênio
        plano_dict['convenio'] = {
            'id': convenio.id,
            'nome': convenio.nome
        }
        
        return jsonify(plano_dict), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@convenio_plano_routes.route('/planos/<int:id>', methods=['PUT'])
def atualizar_plano(id):
    """Atualizar um plano existente"""
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        data = request.get_json()
        
        if 'nome' in data:
            plano.nome = data['nome']
        if 'codigo' in data:
            plano.codigo = data['codigo']
        if 'tipo_acomodacao' in data:
            plano.tipo_acomodacao = data['tipo_acomodacao']
        if 'convenio_id' in data:
            # Verificar se o novo convênio existe
            convenio = Convenio.query.get(data['convenio_id'])
            if not convenio:
                return jsonify({'error': 'Convênio não encontrado'}), 404
            plano.convenio_id = data['convenio_id']
        if 'ativo' in data:
            plano.ativo = data['ativo']
            
        db.session.commit()
        
        plano_dict = plano.to_dict()
        # Adicionar informações do convênio
        convenio = Convenio.query.get(plano.convenio_id)
        if convenio:
            plano_dict['convenio'] = {
                'id': convenio.id,
                'nome': convenio.nome
            }
            
        return jsonify(plano_dict), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@convenio_plano_routes.route('/planos/<int:id>/status', methods=['PATCH'])
def alterar_status_plano(id):
    """Alterar o status de um plano (ativar/desativar)"""
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        data = request.get_json()
        if 'ativo' in data:
            plano.ativo = data['ativo']
            
        db.session.commit()
        
        return jsonify(plano.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500