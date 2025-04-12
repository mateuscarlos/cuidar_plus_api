from flask import Blueprint, request, jsonify
from db import db
from models.pacientes import Paciente
from models.endereco import Endereco
import json
from werkzeug.exceptions import NotFound, BadRequest
from flasgger import swag_from

pacientes_routes = Blueprint('pacientes', __name__)

@pacientes_routes.route('/pacientes/criar', methods=['POST'])
def criar_paciente():
    """
    Criar um novo paciente
    ---
    tags:
      - Pacientes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_completo:
              type: string
              example: "João da Silva"
              description: "Nome completo do paciente"
            cpf:
              type: string
              example: "12345678901"
              description: "CPF do paciente (apenas números)"
            data_nascimento:
              type: string
              example: "01/01/1990"
              description: "Data de nascimento no formato DD/MM/YYYY"
            convenio_id:
              type: integer
              example: 1
              description: "ID do convênio (opcional)"
            plano_id:
              type: integer
              example: 2
              description: "ID do plano (opcional)"
            numero_carteirinha:
              type: string
              example: "123456789"
              description: "Número da carteirinha do convênio (opcional)"
            data_validade:
              type: string
              example: "31/12/2025"
              description: "Data de validade da carteirinha no formato DD/MM/YYYY (opcional)"
            acomodacao:
              type: string
              example: "Apartamento"
              description: "Tipo de acomodação (opcional)"
            telefone:
              type: string
              example: "(11) 98765-4321"
              description: "Telefone principal"
            telefone_secundario:
              type: string
              example: "(11) 3456-7890"
              description: "Telefone secundário (opcional)"
            email:
              type: string
              example: "joao.silva@email.com"
              description: "Email do paciente (opcional)"
            alergias:
              type: string
              example: "Aspirina, Penicilina"
              description: "Lista de alergias do paciente (opcional)"
            cid_primario:
              type: string
              example: "G40"
              description: "CID primário (opcional)"
            cid_secundario:
              type: string
              example: "I10"
              description: "CID secundário (opcional)"
            status:
              type: string
              example: "Ativo"
              description: "Status do paciente (opcional)"
            genero:
              type: string
              example: "Masculino"
              description: "Gênero do paciente (opcional)"
            estado_civil:
              type: string
              example: "Casado"
              description: "Estado civil do paciente (opcional)"
            profissao:
              type: string
              example: "Engenheiro"
              description: "Profissão do paciente (opcional)"
            nacionalidade:
              type: string
              example: "Brasileira"
              description: "Nacionalidade do paciente (opcional)"
            contato_emergencia:
              type: string
              example: "Maria da Silva"
              description: "Nome do contato de emergência (opcional)"
            telefone_emergencia:
              type: string
              example: "(11) 99876-5432"
              description: "Telefone do contato de emergência (opcional)"
            case_responsavel:
              type: string
              example: "Dra. Ana Santos"
              description: "Responsável pelo caso (opcional)"
            medico_responsavel:
              type: string
              example: "Dr. Pedro Rocha"
              description: "Médico responsável (opcional)"
            endereco:
              type: object
              properties:
                cep:
                  type: string
                  example: "01001000"
                logradouro:
                  type: string
                  example: "Praça da Sé"
                numero:
                  type: string
                  example: "123"
                complemento:
                  type: string
                  example: "Apto 45"
                bairro:
                  type: string
                  example: "Sé"
                cidade:
                  type: string
                  example: "São Paulo"
                estado:
                  type: string
                  example: "SP"
          required:
            - nome_completo
            - cpf
            - data_nascimento
    responses:
      201:
        description: Paciente criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome_completo:
              type: string
              example: "João da Silva"
            cpf:
              type: string
              example: "12345678901"
            data_nascimento:
              type: string
              example: "1990-01-01"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Campos obrigatórios não foram preenchidos."
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao criar paciente: mensagem de erro"
    """
    try:
        # Obter os dados do corpo da requisição
        data = request.get_json()

        # Validar os dados obrigatórios
        if not data.get('nome_completo') or not data.get('cpf') or not data.get('data_nascimento'):
            return jsonify({'error': 'Campos obrigatórios não foram preenchidos.'}), 400

        # Converter datas para o formato do banco antes de criar o paciente
        if 'data_nascimento' in data:
            from utils import convert_ddmmyyyy_to_db_format
            try:
                data['data_nascimento'] = convert_ddmmyyyy_to_db_format(data['data_nascimento'])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400

        if 'data_validade' in data:
            from utils import convert_ddmmyyyy_to_db_format
            try:
                data['data_validade'] = convert_ddmmyyyy_to_db_format(data['data_validade'])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400

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
    """
    Buscar pacientes com diferentes critérios
    ---
    tags:
      - Pacientes
    parameters:
      - name: tipo
        in: query
        type: string
        required: true
        description: Tipo de busca (cpf, id, nome)
        enum: [cpf, id, nome]
      - name: valor
        in: query
        type: string
        required: true
        description: Valor a ser buscado
    responses:
      200:
        description: Lista de pacientes encontrados
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome_completo:
                type: string
                example: "João da Silva"
              cpf:
                type: string
                example: "12345678901"
              data_nascimento:
                type: string
                example: "1990-01-01"
              telefone:
                type: string
                example: "(11) 98765-4321"
              email:
                type: string
                example: "joao.silva@email.com"
              status:
                type: string
                example: "Ativo"
      400:
        description: Parâmetros inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Parâmetros tipo e valor são obrigatórios"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao buscar pacientes: mensagem de erro"
    """
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

@pacientes_routes.route('/pacientes/buscar/<int:id>', methods=['GET'])
def obter_paciente(id):
    """
    Obter um paciente pelo ID
    ---
    tags:
      - Pacientes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do paciente
    responses:
      200:
        description: Dados detalhados do paciente
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome_completo:
              type: string
              example: "João da Silva"
            cpf:
              type: string
              example: "12345678901"
            data_nascimento:
              type: string
              example: "1990-01-01"
            convenio_id:
              type: integer
              example: 1
            plano_id:
              type: integer
              example: 2
            numero_carteirinha:
              type: string
              example: "123456789"
            data_validade:
              type: string
              example: "2025-12-31"
            acomodacao:
              type: string
              example: "Apartamento"
            endereco:
              type: object
              properties:
                cep:
                  type: string
                  example: "01001000"
                logradouro:
                  type: string
                  example: "Praça da Sé"
                numero:
                  type: string
                  example: "123"
                complemento:
                  type: string
                  example: "Apto 45"
                bairro:
                  type: string
                  example: "Sé"
                cidade:
                  type: string
                  example: "São Paulo"
                estado:
                  type: string
                  example: "SP"
      404:
        description: Paciente não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Paciente não encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao buscar paciente: mensagem de erro"
    """
    try:
        paciente = Paciente.query.get(id)
        if not paciente:
            return jsonify({'error': 'Paciente não encontrado'}), 404
            
        return jsonify(paciente.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pacientes_routes.route('/pacientes/atualizar/<int:id>', methods=['PUT'])
def atualizar_paciente(id):
    """
    Atualizar um paciente existente
    ---
    tags:
      - Pacientes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do paciente a ser atualizado
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_completo:
              type: string
              example: "João da Silva Atualizado"
            cpf:
              type: string
              example: "12345678901"
            data_nascimento:
              type: string
              example: "01/01/1990"
            convenio_id:
              type: integer
              example: 2
            plano_id:
              type: integer
              example: 3
            numero_carteirinha:
              type: string
              example: "987654321"
            data_validade:
              type: string
              example: "31/12/2026"
            acomodacao:
              type: string
              example: "Enfermaria"
            telefone:
              type: string
              example: "(11) 99876-5432"
            telefone_secundario:
              type: string
              example: "(11) 3456-7890"
            email:
              type: string
              example: "joao.silva.novo@email.com"
            alergias:
              type: string
              example: "Aspirina, Penicilina, Ibuprofeno"
            cid_primario:
              type: string
              example: "G40.1"
            cid_secundario:
              type: string
              example: "I10.0"
            status:
              type: string
              example: "Em Tratamento"
            genero:
              type: string
              example: "Masculino"
            estado_civil:
              type: string
              example: "Casado"
            profissao:
              type: string
              example: "Engenheiro Civil"
            nacionalidade:
              type: string
              example: "Brasileira"
            contato_emergencia:
              type: string
              example: "Maria da Silva"
            telefone_emergencia:
              type: string
              example: "(11) 99888-7777"
            case_responsavel:
              type: string
              example: "Dra. Ana Santos Silva"
            medico_responsavel:
              type: string
              example: "Dr. Pedro Rocha Oliveira"
            endereco:
              type: object
              properties:
                cep:
                  type: string
                  example: "04001000"
                logradouro:
                  type: string
                  example: "Avenida Paulista"
                numero:
                  type: string
                  example: "1000"
                complemento:
                  type: string
                  example: "Sala 123"
                bairro:
                  type: string
                  example: "Bela Vista"
                cidade:
                  type: string
                  example: "São Paulo"
                estado:
                  type: string
                  example: "SP"
    responses:
      200:
        description: Paciente atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome_completo:
              type: string
              example: "João da Silva Atualizado"
            cpf:
              type: string
              example: "12345678901"
            data_nascimento:
              type: string
              example: "1990-01-01"
      404:
        description: Paciente não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Paciente não encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao atualizar paciente: mensagem de erro"
    """
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

@pacientes_routes.route('/pacientes/delete/<int:id>', methods=['DELETE'])
def excluir_paciente(id):
    """
    Excluir um paciente
    ---
    tags:
      - Pacientes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do paciente a ser excluído
    responses:
      200:
        description: Paciente excluído com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Paciente excluído com sucesso"
      404:
        description: Paciente não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Paciente não encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao excluir paciente: mensagem de erro"
    """
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
    """
    Listar todos os pacientes
    ---
    tags:
      - Pacientes
    responses:
      200:
        description: Lista de todos os pacientes
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome_completo:
                type: string
                example: "João da Silva"
              cpf:
                type: string
                example: "12345678901"
              data_nascimento:
                type: string
                example: "1990-01-01"
              telefone:
                type: string
                example: "(11) 98765-4321"
              email:
                type: string
                example: "joao.silva@email.com"
              status:
                type: string
                example: "Ativo"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao listar pacientes: mensagem de erro"
    """
    try:
        pacientes = Paciente.query.all()
        resultado = [paciente.to_dict() for paciente in pacientes]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500