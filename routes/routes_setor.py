from flask import Blueprint, jsonify, request
from models import db, Setor, Funcao

bp = Blueprint('api', __name__, url_prefix='/api')

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
            "conselho_profissional": f.conselho_profissional,
            "especializacao_recomendada": f.especializacao_recomendada,
            "tipo_contratacao": f.tipo_contratacao
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
            "conselho_profissional": f.conselho_profissional,
            "especializacao_recomendada": f.especializacao_recomendada,
            "tipo_contratacao": f.tipo_contratacao
        }
        for f in funcoes
    ])

@bp.route('/funcoes', methods=['POST'])
def create_funcao():
    """Cria uma nova função."""
    data = request.get_json()

    nome = data.get('nome')
    setor_id = data.get('setor_id')
    conselho_profissional = data.get('conselho_profissional')
    tipo_contratacao = data.get('tipo_contratacao')

    if not nome or not setor_id or not tipo_contratacao:
        return jsonify({"error": "Os campos 'nome', 'setor_id' e 'tipo_contratacao' são obrigatórios."}), 400

    # Validação do campo conselho_profissional
    if conselho_profissional is not None and conselho_profissional.strip() == '':
        return jsonify({"error": "O campo 'conselho_profissional' não pode ser vazio."}), 400

    funcao = Funcao(
        nome=nome,
        setor_id=setor_id,
        conselho_profissional=conselho_profissional,
        especializacao_recomendada=data.get('especializacao_recomendada'),
        tipo_contratacao=tipo_contratacao
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
    conselho_profissional = data.get('conselho_profissional')
    tipo_contratacao = data.get('tipo_contratacao')

    if not nome or not setor_id or not tipo_contratacao:
        return jsonify({"error": "Os campos 'nome', 'setor_id' e 'tipo_contratacao' são obrigatórios."}), 400

    # Validação do campo conselho_profissional
    if conselho_profissional is not None and conselho_profissional.strip() == '':
        return jsonify({"error": "O campo 'conselho_profissional' não pode ser vazio."}), 400

    funcao.nome = nome
    funcao.setor_id = setor_id
    funcao.conselho_profissional = conselho_profissional
    funcao.especializacao_recomendada = data.get('especializacao_recomendada')
    funcao.tipo_contratacao = tipo_contratacao

    db.session.commit()
    return jsonify({"id": funcao.id, "nome": funcao.nome}), 200

@bp.route('/funcoes/<int:funcao_id>', methods=['DELETE'])
def delete_funcao(funcao_id):
    """Exclui uma função."""
    funcao = Funcao.query.get_or_404(funcao_id)
    db.session.delete(funcao)
    db.session.commit()
    return jsonify({"message": "Função excluída com sucesso."}), 200
