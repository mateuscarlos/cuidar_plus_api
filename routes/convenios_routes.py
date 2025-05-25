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
      500:
        description: Erro interno
    """
    try:
        convenios = Convenio.query.all()
        resultado = [convenio.to_dict() for convenio in convenios]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar convênios: {str(e)}'}), 500

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
      404:
        description: Convênio não encontrado
      500:
        description: Erro interno
    """
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        return jsonify(convenio.to_dict(include_planos=True)), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar convênio: {str(e)}'}), 500

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
            codigo:
              type: string
              example: "AMIL001"
              description: "Código do convênio"
            telefone:
              type: string
              example: "(11) 1234-5678"
              description: "Telefone de contato"
            email:
              type: string
              example: "contato@amil.com.br"
              description: "E-mail de contato"
            endereco:
              type: string
              example: "Rua das Flores, 123"
              description: "Endereço completo"
            observacoes:
              type: string
              example: "Observações gerais"
              description: "Observações sobre o convênio"
            status:
              type: string
              example: "ATIVO"
              description: "Status do convênio"
          required:
            - nome
    responses:
      201:
        description: Convênio criado com sucesso
      400:
        description: Dados inválidos
      500:
        description: Erro interno
    """
    try:
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'error': 'O nome do convênio é obrigatório'}), 400
        
        # Mapear status para ativo (boolean)
        ativo = True
        if 'status' in data:
            ativo = data.get('status') == 'ATIVO'
        
        novo_convenio = Convenio(
            nome=data.get('nome'),
            codigo=data.get('codigo'),
            telefone=data.get('telefone'),
            email=data.get('email'),
            endereco=data.get('endereco'),
            observacoes=data.get('observacoes'),
            ativo=ativo
        )
        
        db.session.add(novo_convenio)
        db.session.commit()
        
        return jsonify(novo_convenio.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar convênio: {str(e)}'}), 500

@convenios_routes.route('/convenios/<int:id>', methods=['PUT'])
def atualizar_convenio(id):
    """
    Atualizar um convênio existente
    ---
    tags:
      - Convênios
    """
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'error': 'O nome do convênio é obrigatório'}), 400
            
        # Atualizar campos
        convenio.nome = data.get('nome')
        if 'codigo' in data:
            convenio.codigo = data.get('codigo')
        if 'telefone' in data:
            convenio.telefone = data.get('telefone')
        if 'email' in data:
            convenio.email = data.get('email')
        if 'endereco' in data:
            convenio.endereco = data.get('endereco')
        if 'observacoes' in data:
            convenio.observacoes = data.get('observacoes')
        if 'status' in data:
            convenio.ativo = data.get('status') == 'ATIVO'
        
        db.session.commit()
        
        return jsonify(convenio.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar convênio: {str(e)}'}), 500

@convenios_routes.route('/convenios/<int:id>', methods=['DELETE'])
def excluir_convenio(id):
    """
    Excluir um convênio
    ---
    tags:
      - Convênios
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
        return jsonify({'error': f'Erro ao excluir convênio: {str(e)}'}), 500

# PLANOS

@convenios_routes.route('/convenios/<int:id>/planos', methods=['POST'])
def criar_plano(id):
    """
    Criar um novo plano para um convênio
    ---
    tags:
      - Convênios
    """
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'error': 'O nome do plano é obrigatório'}), 400
        
        # Mapear ativo (boolean)
        ativo = True
        if 'ativo' in data:
            ativo = data.get('ativo')
        
        novo_plano = Plano(
            nome=data.get('nome'),
            convenio_id=id,
            codigo=data.get('codigo'),
            descricao=data.get('descricao'),
            tipo_acomodacao=data.get('tipo_acomodacao'),
            cobertura_ambulatorial=data.get('cobertura_ambulatorial', True),
            cobertura_hospitalar=data.get('cobertura_hospitalar', True),
            cobertura_obstetrica=data.get('cobertura_obstetrica', False),
            cobertura_odontologica=data.get('cobertura_odontologica', False),
            cobertura_emergencia=data.get('cobertura_emergencia', True),
            valor_mensalidade=data.get('valor_mensalidade'),
            carencia_consultas=data.get('carencia_consultas', 0),
            carencia_exames=data.get('carencia_exames', 0),
            carencia_internacao=data.get('carencia_internacao', 0),
            observacoes=data.get('observacoes'),
            ativo=ativo
        )
        
        db.session.add(novo_plano)
        db.session.commit()
        
        return jsonify(novo_plano.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar plano: {str(e)}'}), 500

@convenios_routes.route('/planos/convenios/<int:id>', methods=['GET'])
def obter_planos_convenio(id):
    """
    Obter planos de um convênio específico
    ---
    tags:
      - Convênios
    """
    try:
        convenio = Convenio.query.get(id)
        if not convenio:
            return jsonify({'error': 'Convênio não encontrado'}), 404
            
        planos = Plano.query.filter_by(convenio_id=id).all()
        resultado = [p.to_dict() for p in planos]
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar planos do convênio: {str(e)}'}), 500

@convenios_routes.route('/planos', methods=['GET'])
def listar_planos():
    """
    Listar todos os planos
    ---
    tags:
      - Convênios
    """
    try:
        planos = Plano.query.all()
        resultado = [plano.to_dict() for plano in planos]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar planos: {str(e)}'}), 500

@convenios_routes.route('/planos/<int:id>', methods=['GET'])
def obter_plano(id):
    """
    Obter um plano pelo ID
    ---
    tags:
      - Convênios
    """
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        return jsonify(plano.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar plano: {str(e)}'}), 500

@convenios_routes.route('/planos/<int:id>', methods=['PUT'])
def atualizar_plano(id):
    """
    Atualizar um plano existente
    ---
    tags:
      - Convênios
    """
    try:
        plano = Plano.query.get(id)
        if not plano:
            return jsonify({'error': 'Plano não encontrado'}), 404
            
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'error': 'O nome do plano é obrigatório'}), 400
            
        # Atualizar campos
        plano.nome = data.get('nome')
        
        if 'codigo' in data:
            plano.codigo = data.get('codigo')
        if 'descricao' in data:
            plano.descricao = data.get('descricao')
        if 'tipo_acomodacao' in data:
            plano.tipo_acomodacao = data.get('tipo_acomodacao')
        if 'cobertura_ambulatorial' in data:
            plano.cobertura_ambulatorial = data.get('cobertura_ambulatorial')
        if 'cobertura_hospitalar' in data:
            plano.cobertura_hospitalar = data.get('cobertura_hospitalar')
        if 'cobertura_obstetrica' in data:
            plano.cobertura_obstetrica = data.get('cobertura_obstetrica')
        if 'cobertura_odontologica' in data:
            plano.cobertura_odontologica = data.get('cobertura_odontologica')
        if 'cobertura_emergencia' in data:
            plano.cobertura_emergencia = data.get('cobertura_emergencia')
        if 'valor_mensalidade' in data:
            plano.valor_mensalidade = data.get('valor_mensalidade')
        if 'carencia_consultas' in data:
            plano.carencia_consultas = data.get('carencia_consultas')
        if 'carencia_exames' in data:
            plano.carencia_exames = data.get('carencia_exames')
        if 'carencia_internacao' in data:
            plano.carencia_internacao = data.get('carencia_internacao')
        if 'observacoes' in data:
            plano.observacoes = data.get('observacoes')
        if 'ativo' in data:
            plano.ativo = data.get('ativo')
        
        db.session.commit()
        
        return jsonify(plano.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar plano: {str(e)}'}), 500

@convenios_routes.route('/planos/<int:id>/status', methods=['PATCH'])
def alterar_status_plano(id):
    """
    Alterar status de um plano (ativar/desativar)
    ---
    tags:
      - Convênios
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
        return jsonify({'error': f'Erro ao alterar status do plano: {str(e)}'}), 500

@convenios_routes.route('/planos/<int:id>', methods=['DELETE'])
def excluir_plano(id):
    """
    Excluir um plano
    ---
    tags:
      - Convênios
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
        return jsonify({'error': f'Erro ao excluir plano: {str(e)}'}), 500