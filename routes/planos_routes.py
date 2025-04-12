from flask import Blueprint, request, jsonify
from models.plano import Plano
from db import db
from flasgger import swag_from
from werkzeug.exceptions import NotFound, BadRequest

planos_routes = Blueprint('planos_routes', __name__)

@planos_routes.route('/planos', methods=['GET'])
def listar_planos():
    """
    Listar todos os planos de convênios
    ---
    tags:
      - Convênios
    responses:
      200:
        description: Lista de planos
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
                example: "Plano Básico"
              convenio_id:
                type: integer
                example: 2
              descricao:
                type: string
                example: "Plano com cobertura básica de atendimentos"
              created_at:
                type: string
                format: date-time
                example: "2023-01-01T10:00:00"
              updated_at:
                type: string
                format: date-time
                example: "2023-01-01T10:00:00"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao listar planos: mensagem de erro"
    """
    try:
        planos = Plano.query.all()
        resultado = [plano.to_dict() for plano in planos]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar planos: {str(e)}'}), 500

@planos_routes.route('/planos/<int:plano_id>', methods=['GET'])
def obter_plano(plano_id):
    """
    Obter um plano específico pelo ID
    ---
    tags:
      - Convênios
    parameters:
      - name: plano_id
        in: path
        type: integer
        required: true
        description: ID do plano
    responses:
      200:
        description: Detalhes do plano
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: "Plano Básico"
            convenio_id:
              type: integer
              example: 2
            descricao:
              type: string
              example: "Plano com cobertura básica de atendimentos"
            created_at:
              type: string
              format: date-time
              example: "2023-01-01T10:00:00"
            updated_at:
              type: string
              format: date-time
              example: "2023-01-01T10:00:00"
      404:
        description: Plano não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Plano não encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao buscar plano: mensagem de erro"
    """
    try:
        plano = Plano.query.get(plano_id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
        
        return jsonify(plano.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar plano: {str(e)}'}), 500

@planos_routes.route('/planos/convenio/<int:convenio_id>', methods=['GET'])
def listar_planos_por_convenio(convenio_id):
    """
    Listar planos por convênio
    ---
    tags:
      - Convênios
    parameters:
      - name: convenio_id
        in: path
        type: integer
        required: true
        description: ID do convênio
    responses:
      200:
        description: Lista de planos do convênio
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
                example: "Plano Básico"
              convenio_id:
                type: integer
                example: 2
              descricao:
                type: string
                example: "Plano com cobertura básica de atendimentos"
      404:
        description: Nenhum plano encontrado para o convênio
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Nenhum plano encontrado para este convênio"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao listar planos: mensagem de erro"
    """
    try:
        planos = Plano.query.filter_by(convenio_id=convenio_id).all()
        
        if not planos:
            return jsonify({'message': 'Nenhum plano encontrado para este convênio'}), 404
            
        resultado = [plano.to_dict() for plano in planos]
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({'error': f'Erro ao listar planos: {str(e)}'}), 500

@planos_routes.route('/planos/criar', methods=['POST'])
def criar_plano():
    """
    Criar um novo plano
    ---
    tags:
      - Convênios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Plano Premium"
              description: "Nome do plano"
            convenio_id:
              type: integer
              example: 2
              description: "ID do convênio associado"
            descricao:
              type: string
              example: "Plano com cobertura completa incluindo internações e cirurgias"
              description: "Descrição detalhada do plano"
          required:
            - nome
            - convenio_id
    responses:
      201:
        description: Plano criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 3
            nome:
              type: string
              example: "Plano Premium"
            convenio_id:
              type: integer
              example: 2
            descricao:
              type: string
              example: "Plano com cobertura completa incluindo internações e cirurgias"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Nome e convênio são obrigatórios"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao criar plano: mensagem de erro"
    """
    try:
        dados = request.get_json()
        
        # Validação de campos obrigatórios
        if not dados.get('nome') or not dados.get('convenio_id'):
            return jsonify({'error': 'Nome e convênio são obrigatórios'}), 400
        
        novo_plano = Plano(
            nome=dados.get('nome'),
            convenio_id=dados.get('convenio_id'),
            descricao=dados.get('descricao', '')
        )
        
        db.session.add(novo_plano)
        db.session.commit()
        
        return jsonify(novo_plano.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar plano: {str(e)}'}), 500

@planos_routes.route('/planos/atualizar/<int:plano_id>', methods=['PUT'])
def atualizar_plano(plano_id):
    """
    Atualizar um plano existente
    ---
    tags:
      - Convênios
    parameters:
      - name: plano_id
        in: path
        type: integer
        required: true
        description: ID do plano a ser atualizado
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Plano Premium Plus"
              description: "Nome do plano"
            convenio_id:
              type: integer
              example: 2
              description: "ID do convênio associado"
            descricao:
              type: string
              example: "Plano com cobertura completa incluindo internações, cirurgias e atendimento internacional"
              description: "Descrição detalhada do plano"
    responses:
      200:
        description: Plano atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 3
            nome:
              type: string
              example: "Plano Premium Plus"
            convenio_id:
              type: integer
              example: 2
            descricao:
              type: string
              example: "Plano com cobertura completa incluindo internações, cirurgias e atendimento internacional"
      404:
        description: Plano não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Plano não encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao atualizar plano: mensagem de erro"
    """
    try:
        plano = Plano.query.get(plano_id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        dados = request.get_json()
        
        # Atualiza apenas os campos fornecidos
        if 'nome' in dados:
            plano.nome = dados['nome']
        if 'convenio_id' in dados:
            plano.convenio_id = dados['convenio_id']
        if 'descricao' in dados:
            plano.descricao = dados['descricao']
            
        db.session.commit()
        
        return jsonify(plano.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar plano: {str(e)}'}), 500

@planos_routes.route('/planos/excluir/<int:plano_id>', methods=['DELETE'])
def excluir_plano(plano_id):
    """
    Excluir um plano
    ---
    tags:
      - Convênios
    parameters:
      - name: plano_id
        in: path
        type: integer
        required: true
        description: ID do plano a ser excluído
    responses:
      200:
        description: Plano excluído com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Plano excluído com sucesso"
      404:
        description: Plano não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Plano não encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao excluir plano: mensagem de erro"
    """
    try:
        plano = Plano.query.get(plano_id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        db.session.delete(plano)
        db.session.commit()
        
        return jsonify({'message': 'Plano excluído com sucesso'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao excluir plano: {str(e)}'}), 500