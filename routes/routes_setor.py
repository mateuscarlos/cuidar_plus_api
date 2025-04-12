from flask import Blueprint, request, jsonify
from models.setores_funcoes import Setor, Funcao
from db import db
from flasgger import swag_from

# Fixed url_prefix from ' ' to '' (empty string)
bp = Blueprint('api', __name__, url_prefix='')

# -------------------------------
# Rotas para Setores
# -------------------------------

@bp.route('/setores', methods=['GET'])
def get_setores():
    """
    Retorna todos os setores disponíveis
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
    """
    setores = Setor.query.all()
    return jsonify([{"id": s.id, "nome": s.nome} for s in setores])

@bp.route('/setores', methods=['POST'])
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
          required:
            - nome
    responses:
      201:
        description: Setor criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 2
            nome:
              type: string
              example: "Fisioterapia"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "O campo 'nome' é obrigatório."
    """
    data = request.get_json()
    nome = data.get('nome')

    if not nome:
        return jsonify({"error": "O campo 'nome' é obrigatório."}), 400

    setor = Setor(nome=nome)
    db.session.add(setor)
    db.session.commit()
    return jsonify({"id": setor.id, "nome": setor.nome}), 201

@bp.route('/setores/<int:setor_id>', methods=['PUT'])
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
          required:
            - nome
    responses:
      200:
        description: Setor atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 2
            nome:
              type: string
              example: "Fisioterapia Atualizado"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "O campo 'nome' é obrigatório."
      404:
        description: Setor não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Setor não encontrado"
    """
    data = request.get_json()
    setor = Setor.query.get_or_404(setor_id)

    nome = data.get('nome')
    if not nome:
        return jsonify({"error": "O campo 'nome' é obrigatório."}), 400

    setor.nome = nome
    db.session.commit()
    return jsonify({"id": setor.id, "nome": setor.nome}), 200

@bp.route('/setores/<int:setor_id>', methods=['DELETE'])
def delete_setor(setor_id):
    """
    Exclui um setor
    ---
    tags:
      - Setores
    parameters:
      - name: setor_id
        in: path
        type: integer
        required: true
        description: ID do setor a ser excluído
    responses:
      200:
        description: Setor excluído com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Setor excluído com sucesso."
      404:
        description: Setor não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Setor não encontrado"
    """
    setor = Setor.query.get_or_404(setor_id)
    db.session.delete(setor)
    db.session.commit()
    return jsonify({"message": "Setor excluído com sucesso."}), 200

# -------------------------------
# Rotas para Funções
# -------------------------------

@bp.route('/funcoes', methods=['GET'])
def get_funcoes():
    """
    Retorna todas as funções disponíveis
    ---
    tags:
      - Funções
    responses:
      200:
        description: Lista de funções
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
                example: "Enfermeiro"
              setor_id:
                type: integer
                example: 1
              especializacao_recomendada:
                type: string
                example: "Enfermagem Clínica"
    """
    funcoes = Funcao.query.all()
    return jsonify([
        {
            "id": f.id,
            "nome": f.nome,
            "setor_id": f.setor_id,
            "especializacao_recomendada": f.especializacao_recomendada
        }
        for f in funcoes
    ])

@bp.route('/funcoes/<int:setor_id>', methods=['GET'])
def get_funcoes_por_setor(setor_id):
    """
    Retorna as funções de um setor específico
    ---
    tags:
      - Funções
    parameters:
      - name: setor_id
        in: path
        type: integer
        required: true
        description: ID do setor
    responses:
      200:
        description: Lista de funções do setor
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
                example: "Enfermeiro"
              especializacao_recomendada:
                type: string
                example: "Enfermagem Clínica"
      404:
        description: Nenhuma função encontrada para o setor ou setor não existe
        schema:
          type: array
          items: {}
    """
    funcoes = Funcao.query.filter_by(setor_id=setor_id).all()
    if not funcoes:
        return jsonify([]), 404
    return jsonify([
        {
            "id": f.id,
            "nome": f.nome,
            "especializacao_recomendada": f.especializacao_recomendada,
        }
        for f in funcoes
    ])

@bp.route('/funcoes', methods=['POST'])
def create_funcao():
    """
    Cria uma nova função
    ---
    tags:
      - Funções
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Fisioterapeuta"
            setor_id:
              type: integer
              example: 2
            especializacao_recomendada:
              type: string
              example: "Fisioterapia Ortopédica"
          required:
            - nome
            - setor_id
    responses:
      201:
        description: Função criada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 3
            nome:
              type: string
              example: "Fisioterapeuta"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Os campos 'nome' e 'setor_id' são obrigatórios."
    """
    data = request.get_json()

    nome = data.get('nome')
    setor_id = data.get('setor_id')

    if not nome or not setor_id:
        return jsonify({"error": "Os campos 'nome' e 'setor_id' são obrigatórios."}), 400

    funcao = Funcao(
        nome=nome,
        setor_id=setor_id,
        especializacao_recomendada=data.get('especializacao_recomendada')
    )
    db.session.add(funcao)
    db.session.commit()
    return jsonify({"id": funcao.id, "nome": funcao.nome}), 201

@bp.route('/funcoes/<int:funcao_id>', methods=['PUT'])
def update_funcao(funcao_id):
    """
    Atualiza uma função existente
    ---
    tags:
      - Funções
    parameters:
      - name: funcao_id
        in: path
        type: integer
        required: true
        description: ID da função
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Fisioterapeuta Sênior"
            setor_id:
              type: integer
              example: 2
            especializacao_recomendada:
              type: string
              example: "Fisioterapia Ortopédica e Esportiva"
          required:
            - nome
            - setor_id
    responses:
      200:
        description: Função atualizada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 3
            nome:
              type: string
              example: "Fisioterapeuta Sênior"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Os campos 'nome' e 'setor_id' são obrigatórios."
      404:
        description: Função não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Função não encontrada"
    """
    data = request.get_json()
    funcao = Funcao.query.get_or_404(funcao_id)

    nome = data.get('nome')
    setor_id = data.get('setor_id')

    if not nome or not setor_id:
        return jsonify({"error": "Os campos 'nome' e 'setor_id' são obrigatórios."}), 400

    funcao.nome = nome
    funcao.setor_id = setor_id
    funcao.especializacao_recomendada = data.get('especializacao_recomendada')

    db.session.commit()
    return jsonify({"id": funcao.id, "nome": funcao.nome}), 200

@bp.route('/funcoes/<int:funcao_id>', methods=['DELETE'])
def delete_funcao(funcao_id):
    """
    Exclui uma função
    ---
    tags:
      - Funções
    parameters:
      - name: funcao_id
        in: path
        type: integer
        required: true
        description: ID da função a ser excluída
    responses:
      200:
        description: Função excluída com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Função excluída com sucesso."
      404:
        description: Função não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Função não encontrada"
    """
    funcao = Funcao.query.get_or_404(funcao_id)
    db.session.delete(funcao)
    db.session.commit()
    return jsonify({"message": "Função excluída com sucesso."}), 200

# -------------------------------
# Rotas para Dicionários
# -------------------------------

setores_funcoes_bp = Blueprint('setores_funcoes', __name__)

@setores_funcoes_bp.route('/setores/dicionario', methods=['GET'])
def get_setores_dicionario():
    """
    Retorna um dicionário de todos os setores
    ---
    tags:
      - Dicionários
    responses:
      200:
        description: Dicionário de setores
        schema:
          type: object
          additionalProperties:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: "Enfermagem"
        examples:
          application/json: {
            "1": {"id": 1, "nome": "Enfermagem"},
            "2": {"id": 2, "nome": "Fisioterapia"}
          }
    """
    setores_dict = Setor.get_setores_dict()
    return jsonify(setores_dict)

@setores_funcoes_bp.route('/funcoes/dicionario', methods=['GET'])
def get_funcoes_dicionario():
    """
    Retorna um dicionário de todas as funções
    ---
    tags:
      - Dicionários
    responses:
      200:
        description: Dicionário de funções
        schema:
          type: object
          additionalProperties:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: "Enfermeiro"
              setor_id:
                type: integer
                example: 1
              especializacao_recomendada:
                type: string
                example: "Enfermagem Clínica"
        examples:
          application/json: {
            "1": {"id": 1, "nome": "Enfermeiro", "setor_id": 1, "especializacao_recomendada": "Enfermagem Clínica"},
            "2": {"id": 2, "nome": "Fisioterapeuta", "setor_id": 2, "especializacao_recomendada": "Fisioterapia Ortopédica"}
          }
    """
    funcoes_dict = Funcao.get_funcoes_dict()
    return jsonify(funcoes_dict)

@setores_funcoes_bp.route('/setores/dicionario/<int:setor_id>', methods=['GET'])
def get_setor_by_id(setor_id):
    """
    Retorna um setor específico no formato de dicionário
    ---
    tags:
      - Dicionários
    parameters:
      - name: setor_id
        in: path
        type: integer
        required: true
        description: ID do setor
    responses:
      200:
        description: Dados do setor
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: "Enfermagem"
      404:
        description: Setor não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Setor não encontrado"
    """
    setor = Setor.query.get_or_404(setor_id)
    return jsonify({
        "id": setor.id,
        "nome": setor.nome
    })

@setores_funcoes_bp.route('/funcoes/dicionario/<int:funcao_id>', methods=['GET'])
def get_funcao_by_id(funcao_id):
    """
    Retorna uma função específica no formato de dicionário
    ---
    tags:
      - Dicionários
    parameters:
      - name: funcao_id
        in: path
        type: integer
        required: true
        description: ID da função
    responses:
      200:
        description: Dados da função
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: "Enfermeiro"
            setor_id:
              type: integer
              example: 1
            especializacao_recomendada:
              type: string
              example: "Enfermagem Clínica"
      404:
        description: Função não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Função não encontrada"
    """
    funcao = Funcao.query.get_or_404(funcao_id)
    return jsonify({
        "id": funcao.id,
        "nome": funcao.nome,
        "setor_id": funcao.setor_id,
        "especializacao_recomendada": funcao.especializacao_recomendada
    })

@setores_funcoes_bp.route('/setores/<int:setor_id>/funcoes/dicionario', methods=['GET'])
def get_funcoes_by_setor_dicionario(setor_id):
    """
    Retorna todas as funções de um setor específico no formato de dicionário
    ---
    tags:
      - Dicionários
    parameters:
      - name: setor_id
        in: path
        type: integer
        required: true
        description: ID do setor
    responses:
      200:
        description: Dicionário de funções do setor
        schema:
          type: object
          additionalProperties:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: "Enfermeiro"
              especializacao_recomendada:
                type: string
                example: "Enfermagem Clínica"
        examples:
          application/json: {
            "1": {"id": 1, "nome": "Enfermeiro", "especializacao_recomendada": "Enfermagem Clínica"},
            "2": {"id": 2, "nome": "Técnico de Enfermagem", "especializacao_recomendada": "Enfermagem Hospitalar"}
          }
      404:
        description: Setor não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Setor não encontrado"
    """
    # Verifica se o setor existe
    Setor.query.get_or_404(setor_id)
    
    # Obtém todas as funções do setor
    funcoes = Funcao.query.filter_by(setor_id=setor_id).all()
    
    funcoes_dict = {}
    for funcao in funcoes:
        funcoes_dict[funcao.id] = {
            "id": funcao.id,
            "nome": funcao.nome,
            "especializacao_recomendada": funcao.especializacao_recomendada
        }
    
    return jsonify(funcoes_dict)
