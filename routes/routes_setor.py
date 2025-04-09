# Change the import statement
from flask import Blueprint, request, jsonify
from models.setores_funcoes import Setor, Funcao  # Import models directly
from db import db  # Import db directly

# Fixed url_prefix from ' ' to '' (empty string)
bp = Blueprint('api', __name__, url_prefix='')

# -------------------------------
# Rotas para Setores
# -------------------------------

@bp.route('/setores', methods=['GET'])
def get_setores():
    """Retorna todos os setores disponíveis."""
    setores = Setor.query.all()
    return jsonify([{"id": s.id, "nome": s.nome} for s in setores])

@bp.route('/setores', methods=['POST'])
def create_setor():
    """Cria um novo setor."""
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
    """Atualiza um setor existente."""
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
    """Exclui um setor."""
    setor = Setor.query.get_or_404(setor_id)
    db.session.delete(setor)
    db.session.commit()
    return jsonify({"message": "Setor excluído com sucesso."}), 200

# -------------------------------
# Rotas para Funções
# -------------------------------

@bp.route('/funcoes', methods=['GET'])
def get_funcoes():
    """Retorna todas as funções disponíveis."""
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
    """Retorna as funções de um setor específico."""
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
    """Cria uma nova função."""
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
    """Atualiza uma função existente."""
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
    """Exclui uma função."""
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
    setores_dict = Setor.get_setores_dict()
    return jsonify(setores_dict)

@setores_funcoes_bp.route('/funcoes/dicionario', methods=['GET'])
def get_funcoes_dicionario():
    funcoes_dict = Funcao.get_funcoes_dict()
    return jsonify(funcoes_dict)
