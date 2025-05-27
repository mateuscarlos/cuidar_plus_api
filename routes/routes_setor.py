from flask import Blueprint, request, jsonify
from models.setor import Setor
from db import db

setor_bp = Blueprint('setor', __name__)

@setor_bp.route('/api/setores', methods=['GET'])
def get_setores():
    """
    Retorna todos os setores ativos
    ---
    tags:
      - Setores
    responses:
      200:
        description: Lista de setores
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: "Enfermagem"
              descricao:
                type: string
                example: "Setor de enfermagem"
              status:
                type: boolean
                example: true
    """
    try:
        setores = Setor.query.filter_by(status=True).all()
        return jsonify([setor.to_dict() for setor in setores])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@setor_bp.route('/api/setores', methods=['POST'])
def create_setor():
    """
    Cria um novo setor
    ---
    tags:
      - Setores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Fisioterapia"
            descricao:
              type: string
              example: "Setor de fisioterapia"
          required:
            - nome
    responses:
      201:
        description: Setor criado com sucesso
      400:
        description: Dados inválidos ou setor já existe
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('nome'):
            return jsonify({'error': 'O campo nome é obrigatório'}), 400
        
        # Verificar se já existe um setor com o mesmo nome
        existing_setor = Setor.query.filter_by(nome=data['nome']).first()
        if existing_setor:
            return jsonify({'error': 'Setor já existe'}), 400
        
        setor = Setor()
        setor.nome = data['nome']
        setor.descricao = data.get('descricao')
        setor.status = data.get('status', True)
        
        db.session.add(setor)
        db.session.commit()
        
        return jsonify(setor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@setor_bp.route('/api/setores/<int:setor_id>', methods=['PUT'])
def update_setor(setor_id):
    """
    Atualiza um setor existente
    ---
    tags:
      - Setores
    parameters:
      - name: setor_id
        in: path
        type: integer
        required: true
        description: ID do setor
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Fisioterapia Atualizado"
            descricao:
              type: string
              example: "Descrição atualizada"
    responses:
      200:
        description: Setor atualizado com sucesso
      404:
        description: Setor não encontrado
    """
    try:
        setor = Setor.query.get_or_404(setor_id)
        data = request.get_json()
        
        setor.nome = data.get('nome', setor.nome)
        setor.descricao = data.get('descricao', setor.descricao)
        setor.status = data.get('status', setor.status)
        
        db.session.commit()
        
        return jsonify(setor.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@setor_bp.route('/api/setores/<int:setor_id>', methods=['DELETE'])
def delete_setor(setor_id):
    """
    Desativa um setor (soft delete)
    ---
    tags:
      - Setores
    parameters:
      - name: setor_id
        in: path
        type: integer
        required: true
        description: ID do setor a ser desativado
    responses:
      200:
        description: Setor desativado com sucesso
      404:
        description: Setor não encontrado
    """
    try:
        setor = Setor.query.get_or_404(setor_id)
        setor.status = False  # Soft delete
        db.session.commit()
        
        return jsonify({'message': 'Setor desativado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
