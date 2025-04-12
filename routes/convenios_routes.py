from flask import Blueprint, request, jsonify
from db import db
from models.convenio import Convenio
from models.plano import Plano
from flasgger import swag_from

convenios_routes = Blueprint('convenios_routes', __name__)

# CONVÊNIOS

@convenios_routes.route('/convenios/listar', methods=['GET'])
def listar_convenios():
    """
    Listar todos os convênios
    ---
    tags:
      - Convênios
    responses:
      200:
        description: Lista de convênios
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
                example: "Unimed"
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
              example: "Erro ao listar convênios"
    """
    try:
        convenios = Convenio.query.all()
        resultado = [convenio.to_dict() for convenio in convenios]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/convenios/<int:id>', methods=['GET'])
def obter_convenio(id):
    """
    Obter um convênio pelo ID
    ---
    tags:
      - Convênios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do convênio
    responses:
      200:
        description: Detalhes do convênio
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: "Unimed"
            created_at:
              type: string
              format: date-time
              example: "2023-01-01T10:00:00"
            updated_at:
              type: string
              format: date-time
              example: "2023-01-01T10:00:00"
      404:
        description: Convênio não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Convênio não encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao buscar convênio"
    """
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        return jsonify(convenio.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/convenios/criar', methods=['POST'])
def criar_convenio():
    """
    Criar um novo convênio
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
              example: "Amil"
              description: "Nome do convênio"
          required:
            - nome
    responses:
      201:
        description: Convênio criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 2
            nome:
              type: string
              example: "Amil"
            created_at:
              type: string
              format: date-time
              example: "2023-01-15T14:30:00"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "O nome do convênio é obrigatório"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao criar convênio"
    """
    try:
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'error': 'O nome do convênio é obrigatório'}), 400
        
        novo_convenio = Convenio(nome=data.get('nome'))
        
        db.session.add(novo_convenio)
        db.session.commit()
        
        return jsonify(novo_convenio.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/planos/convenios/<int:id>', methods=['GET'])
def obter_planos_convenio(id):
    """
    Obter planos de um convênio específico
    ---
    tags:
      - Convênios
    parameters:
      - name: id
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
                example: 1
              descricao:
                type: string
                example: "Plano com cobertura básica"
              created_at:
                type: string
                format: date-time
                example: "2023-01-01T10:00:00"
              updated_at:
                type: string
                format: date-time
                example: "2023-01-01T10:00:00"
      404:
        description: Convênio não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Convênio não encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao buscar planos do convênio"
    """
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
    """
    Criar um novo plano para um convênio
    ---
    tags:
      - Convênios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do convênio
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
            descricao:
              type: string
              example: "Plano com cobertura completa"
              description: "Descrição detalhada do plano (opcional)"
          required:
            - nome
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
              example: 1
            descricao:
              type: string
              example: "Plano com cobertura completa"
            created_at:
              type: string
              format: date-time
              example: "2023-01-15T14:30:00"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "O nome do plano é obrigatório"
      404:
        description: Convênio não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Convênio não encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao criar plano"
    """
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'error': 'O nome do plano é obrigatório'}), 400
        
        novo_plano = Plano(
            nome=data.get('nome'),
            convenio_id=id,
            descricao=data.get('descricao', '')
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
    """
    Listar todos os planos
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
                example: 1
              descricao:
                type: string
                example: "Plano com cobertura básica"
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
              example: "Erro ao listar planos"
    """
    try:
        planos = Plano.query.all()
        resultado = [plano.to_dict() for plano in planos]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/planos/<int:id>', methods=['GET'])
def obter_plano(id):
    """
    Obter um plano pelo ID
    ---
    tags:
      - Convênios
    parameters:
      - name: id
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
              example: 1
            descricao:
              type: string
              example: "Plano com cobertura básica"
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
              example: "Erro ao buscar plano"
    """
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        return jsonify(plano.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/planos/<int:id>', methods=['PUT'])
def atualizar_plano(id):
    """
    Atualizar um plano existente
    ---
    tags:
      - Convênios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do plano
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Plano Básico Plus"
              description: "Nome atualizado do plano"
            descricao:
              type: string
              example: "Plano com cobertura básica e alguns adicionais"
              description: "Descrição atualizada do plano (opcional)"
            convenio_id:
              type: integer
              example: 2
              description: "ID do convênio (opcional, para transferir o plano)"
          required:
            - nome
    responses:
      200:
        description: Plano atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: "Plano Básico Plus"
            convenio_id:
              type: integer
              example: 2
            descricao:
              type: string
              example: "Plano com cobertura básica e alguns adicionais"
            updated_at:
              type: string
              format: date-time
              example: "2023-01-15T14:30:00"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "O nome do plano é obrigatório"
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
              example: "Erro ao atualizar plano"
    """
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'error': 'O nome do plano é obrigatório'}), 400
            
        plano.nome = data.get('nome')
        
        if 'descricao' in data:
            plano.descricao = data.get('descricao')
            
        if 'convenio_id' in data:
            plano.convenio_id = data.get('convenio_id')
        
        db.session.commit()
        
        return jsonify(plano.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/planos/<int:id>/status', methods=['PATCH'])
def alterar_status_plano(id):
    """
    Alterar status de um plano (ativar/desativar)
    ---
    tags:
      - Convênios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do plano
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            ativo:
              type: boolean
              example: false
              description: "Status do plano (true = ativo, false = inativo)"
          required:
            - ativo
    responses:
      200:
        description: Status do plano alterado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: "Plano Básico"
            ativo:
              type: boolean
              example: false
            updated_at:
              type: string
              format: date-time
              example: "2023-01-15T14:30:00"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "O campo 'ativo' é obrigatório"
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
              example: "Erro ao alterar status do plano"
    """
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        data = request.get_json()
        
        if 'ativo' not in data:
            return jsonify({'error': "O campo 'ativo' é obrigatório"}), 400
            
        plano.ativo = data.get('ativo')
        
        db.session.commit()
        
        return jsonify(plano.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Adicionando novas rotas para completar CRUD de convênios

@convenios_routes.route('/convenios/<int:id>', methods=['PUT'])
def atualizar_convenio(id):
    """
    Atualizar um convênio existente
    ---
    tags:
      - Convênios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do convênio
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Unimed Nacional"
              description: "Nome atualizado do convênio"
          required:
            - nome
    responses:
      200:
        description: Convênio atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: "Unimed Nacional"
            updated_at:
              type: string
              format: date-time
              example: "2023-01-15T14:30:00"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "O nome do convênio é obrigatório"
      404:
        description: Convênio não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Convênio não encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao atualizar convênio"
    """
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'error': 'O nome do convênio é obrigatório'}), 400
            
        convenio.nome = data.get('nome')
        
        db.session.commit()
        
        return jsonify(convenio.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/convenios/<int:id>', methods=['DELETE'])
def excluir_convenio(id):
    """
    Excluir um convênio
    ---
    tags:
      - Convênios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do convênio a ser excluído
    responses:
      200:
        description: Convênio excluído com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Convênio excluído com sucesso"
      404:
        description: Convênio não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Convênio não encontrado"
      409:
        description: Conflito - Convênio possui planos associados
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Não é possível excluir o convênio, pois existem planos associados"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao excluir convênio"
    """
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        # Verificar se existem planos associados ao convênio
        planos = Plano.query.filter_by(convenio_id=id).first()
        if planos:
            return jsonify({'error': 'Não é possível excluir o convênio, pois existem planos associados'}), 409
            
        db.session.delete(convenio)
        db.session.commit()
        
        return jsonify({'message': 'Convênio excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@convenios_routes.route('/planos/<int:id>', methods=['DELETE'])
def excluir_plano(id):
    """
    Excluir um plano
    ---
    tags:
      - Convênios
    parameters:
      - name: id
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
      409:
        description: Conflito - Plano possui pacientes associados
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Não é possível excluir o plano, pois existem pacientes associados"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao excluir plano"
    """
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        # Verificar se existem pacientes usando este plano
        # Esta verificação depende da estrutura do seu modelo de paciente
        # Exemplo: pacientes = Paciente.query.filter_by(plano_id=id).first()
        
        db.session.delete(plano)
        db.session.commit()
        
        return jsonify({'message': 'Plano excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500