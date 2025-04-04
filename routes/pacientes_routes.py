from flask import Blueprint, request, jsonify
from db import db
from models.pacientes import Paciente
from models.endereco import Endereco
from models.convenio import Convenio  # Adicionar importação
from models.plano import Plano  # Adicionar importação
import json
from werkzeug.exceptions import NotFound, BadRequest

pacientes_routes = Blueprint('pacientes', __name__)

@pacientes_routes.route('/pacientes/criar', methods=['POST'])
def criar_paciente():
    """Criar um novo paciente"""
    try:
        # Obter os dados do corpo da requisição
        data = request.get_json()

        # Validar campos obrigatórios
        campos_obrigatorios = ['nome_completo', 'cpf', 'data_nascimento', 'telefone',
                              'cid_primario', 'acomodacao', 'convenio_id', 'plano_id',
                              'numero_carteirinha', 'data_validade']
        
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'error': f'O campo {campo} é obrigatório.'}), 400

        # Verificar se o convênio existe
        convenio_id = data.get('convenio_id')
        if convenio_id:
            convenio = Convenio.query.filter_by(id=convenio_id, ativo=True).first()
            if not convenio:
                return jsonify({'error': 'O convênio selecionado não existe ou está inativo.'}), 400

        # Verificar se o plano existe e pertence ao convênio
        plano_id = data.get('plano_id')
        convenio_id = data.get('convenio_id')
        if plano_id and convenio_id:
            plano = Plano.query.get(plano_id)
            if not plano:
                return jsonify({'error': 'O plano selecionado não existe.'}), 400
            if plano.convenio_id != convenio_id:
                return jsonify({'error': 'O plano selecionado não pertence ao convênio informado.'}), 400

        # Criar o paciente a partir do dicionário
        novo_paciente = Paciente.from_dict(data)

        # Salvar no banco de dados
        db.session.add(novo_paciente)
        db.session.commit()

        return jsonify(novo_paciente.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pacientes_routes.route('/pacientes/buscar', methods=['GET'])
def buscar_pacientes():
    """Buscar pacientes com diferentes critérios"""
    try:
        tipo = request.args.get('tipo')
        valor = request.args.get('valor')
        
        if not tipo or not valor:
            return jsonify({'error': 'Parâmetros tipo e valor são obrigatórios'}), 400
            
        if tipo == 'cpf':
            pacientes = Paciente.query.filter(Paciente.cpf.like(f'%{valor}%')).all()
        elif tipo == 'id':
            pacientes = Paciente.query.filter(Paciente.id == int(valor)).all() if valor.isdigit() else []
        elif tipo == 'nome':
            pacientes = Paciente.query.filter(Paciente.nome_completo.ilike(f'%{valor}%')).all()
        else:
            return jsonify({'error': 'Tipo de busca inválido'}), 400
            
        resultado = [p.to_dict() for p in pacientes]
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pacientes_routes.route('/pacientes/<int:id>', methods=['GET'])
def obter_paciente(id):
    """Obter um paciente pelo ID"""
    try:
        paciente = Paciente.query.get(id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
            
        return jsonify(paciente.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pacientes_routes.route('/pacientes/<int:id>', methods=['PUT'])
def atualizar_paciente(id):
    """Atualizar um paciente existente"""
    try:
        paciente = Paciente.query.get(id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
            
        data = request.get_json()
        
        # Atualizar campos básicos
        if 'nome_completo' in data:
            paciente.nome_completo = data['nome_completo']
        if 'convenio_id' in data:
            paciente.convenio_id = data['convenio_id']
        if 'plano_id' in data:
            paciente.plano_id = data['plano_id']
        if 'numero_carteirinha' in data:
            paciente.numero_carteirinha = data['numero_carteirinha']
        if 'acomodacao' in data:
            paciente.acomodacao = data['acomodacao']
        if 'telefone' in data:
            paciente.telefone = data['telefone']
        if 'telefone_secundario' in data:
            paciente.telefone_secundario = data['telefone_secundario']
        if 'email' in data:
            paciente.email = data['email']
        if 'alergias' in data:
            paciente.alergias = data['alergias']
        if 'cid_primario' in data:
            paciente.cid_primario = data['cid_primario']
        if 'cid_secundario' in data:
            paciente.cid_secundario = data['cid_secundario']
        if 'status' in data:
            paciente.status = data['status']
        if 'genero' in data:
            paciente.genero = data['genero']
        if 'estado_civil' in data:
            paciente.estado_civil = data['estado_civil']
        if 'profissao' in data:
            paciente.profissao = data['profissao']
        if 'nacionalidade' in data:
            paciente.nacionalidade = data['nacionalidade']
        if 'contato_emergencia' in data:
            paciente.contato_emergencia = data['contato_emergencia']
        if 'telefone_emergencia' in data:
            paciente.telefone_emergencia = data['telefone_emergencia']
        if 'case_responsavel' in data:
            paciente.case_responsavel = data['case_responsavel']
        if 'medico_responsavel' in data:
            paciente.medico_responsavel = data['medico_responsavel']
            
        # Tratar datas
        if 'data_nascimento' in data:
            from utils import convert_ddmmyyyy_to_db_format
            paciente.data_nascimento = convert_ddmmyyyy_to_db_format(data['data_nascimento'])
            
        if 'data_validade' in data:
            from utils import convert_ddmmyyyy_to_db_format
            paciente.data_validade = convert_ddmmyyyy_to_db_format(data['data_validade'])
            
        # Atualizar endereço se fornecido
        if 'endereco' in data and data['endereco']:
            endereco = Endereco.from_dict(data['endereco'])
            paciente.endereco = endereco
            
        db.session.commit()
        
        return jsonify(paciente.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pacientes_routes.route('/pacientes/<int:id>', methods=['DELETE'])
def excluir_paciente(id):
    """Excluir um paciente"""
    try:
        paciente = Paciente.query.get(id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
            
        db.session.delete(paciente)
        db.session.commit()
        
        return jsonify({'message': 'Paciente excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pacientes_routes.route('/pacientes', methods=['GET'])
def listar_todos_pacientes():
    """Listar todos os pacientes"""
    try:
        pacientes = Paciente.query.all()
        resultado = [paciente.to_dict() for paciente in pacientes]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500