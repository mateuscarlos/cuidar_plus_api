from flask import Blueprint, request, jsonify
import requests
from models.pacientes import Paciente
from db import db
from flasgger import Swagger
from utils import validate_cpf, sanitize_input, get_local_time, get_user_timezone
from werkzeug.exceptions import BadRequest, Conflict, NotFound
import re
from datetime import datetime, timezone

pacientes_routes = Blueprint('pacientes_routes', __name__)

def get_address_from_cep(cep):
    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    if response.status_code != 200:
        raise BadRequest("CEP inválido")
    data = response.json()
    if 'erro' in data:
        raise BadRequest("CEP inválido")
    return data

@pacientes_routes.route('/api/criar_paciente', methods=['POST'])
def create_paciente():
    """
    Cria um novo paciente
    ---
    tags:
      - Pacientes
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nome_completo
            - cpf
            - operadora
            - cid_primario
            - cep
          properties:
            nome_completo:
              type: string
              description: Nome completo do paciente
            cpf:
              type: string
              description: CPF do paciente
            operadora:
              type: string
              description: Operadora do paciente
            cid_primario:
              type: string
              description: CID primário do paciente
            rua:
              type: string
              description: Rua do paciente
            numero:
              type: string
              description: Número da residência do paciente
            complemento:
              type: string
              description: Complemento da residência do paciente
            cep:
              type: string
              description: CEP do paciente
    responses:
      201:
        description: Paciente criado com sucesso
      400:
        description: Campos obrigatórios faltando ou CPF/CEP inválido
      409:
        description: CPF já cadastrado
      500:
        description: Erro interno no servidor
    """
    try:
        data = request.get_json()
        required_fields = ['nome_completo', 'cpf', 'operadora', 'cid_primario', 'cep']
        if not all(field in data for field in required_fields):
            raise BadRequest("Campos obrigatórios faltando: nome_completo, cpf, operadora, cid_primario, cep")
        
        cpf = re.sub(r'[^\d]', '', data['cpf'])
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        if Paciente.query.filter_by(cpf=cpf).first():
            raise Conflict("CPF já cadastrado")

        address_data = get_address_from_cep(data['cep'])

        paciente_data = {
            'nome_completo': sanitize_input(str(data['nome_completo']), 100),
            'cpf': cpf,
            'operadora': sanitize_input(str(data['operadora']), 50),
            'cid_primario': sanitize_input(str(data['cid_primario']), 10),
            'rua': address_data.get('logradouro', ''),
            'numero': sanitize_input(str(data.get('numero')), 10) if data.get('numero') else None,
            'complemento': sanitize_input(str(data.get('complemento')), 50) if data.get('complemento') else None,
            'cep': data['cep'],
            'cidade': address_data.get('localidade', ''),
            'estado': address_data.get('uf', ''),
            'updated_at': datetime.now(timezone.utc)
        }

        new_paciente = Paciente(**paciente_data)
        db.session.add(new_paciente)
        db.session.commit()

        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)

        return jsonify({
            'message': 'Paciente criado com sucesso!',
            'id': new_paciente.id,
            'updated_at': get_local_time(new_paciente.updated_at, user_timezone).isoformat()
        }), 201

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except Conflict as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500

@pacientes_routes.route('/api/exibe_pacientes', methods=['GET'])
def get_all_pacientes():
    """
    Exibe todos os pacientes
    ---
    tags:
      - Pacientes
    responses:
      200:
        description: Lista de pacientes
      500:
        description: Erro ao recuperar pacientes
    """
    try:
        pacientes = Paciente.query.all()
        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)
        
        return jsonify({
            'pacientes': [{
                'id': p.id,
                'nome_completo': p.nome_completo,
                'cpf': p.cpf,
                'operadora': p.operadora,
                'cid_primario': p.cid_primario,
                'rua': p.rua,
                'numero': p.numero,
                'complemento': p.complemento,
                'cep': p.cep,
                'cidade': p.cidade,
                'estado': p.estado,
                'updated_at': get_local_time(p.updated_at, user_timezone).isoformat()
            } for p in pacientes]
        }), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao recuperar pacientes', 'error': str(e)}), 500

@pacientes_routes.route('/api/atualizar_paciente/<cpf>', methods=['PUT'])
def atualizar_paciente(cpf):
    """
    Atualiza um paciente existente
    ---
    tags:
      - Pacientes
    parameters:
      - in: path
        name: cpf
        type: string
        required: true
        description: CPF do paciente
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome_completo:
              type: string
              description: Nome completo do paciente
            operadora:
              type: string
              description: Operadora do paciente
            cid_primario:
              type: string
              description: CID primário do paciente
            rua:
              type: string
              description: Rua do paciente
            numero:
              type: string
              description: Número da residência do paciente
            complemento:
              type: string
              description: Complemento da residência do paciente
            cep:
              type: string
              description: CEP do paciente
            cidade:
              type: string
              description: Cidade do paciente
            estado:
              type: string
              description: Estado do paciente
    responses:
      200:
        description: Paciente atualizado com sucesso
      400:
        description: CPF inválido
      404:
        description: Paciente não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        paciente = Paciente.query.filter_by(cpf=cpf).first()
        if not paciente:
            raise NotFound("Paciente não encontrado")

        data = request.get_json()
        update_fields = {
            'nome_completo': sanitize_input(data.get('nome_completo'), 100) if data.get('nome_completo') else None,
            'operadora': sanitize_input(data.get('operadora'), 50) if data.get('operadora') else None,
            'cid_primario': sanitize_input(data.get('cid_primario'), 10) if data.get('cid_primario') else None,
            'rua': sanitize_input(data.get('rua'), 100) if data.get('rua') else None,
            'numero': sanitize_input(data.get('numero'), 10) if data.get('numero') else None,
            'complemento': sanitize_input(data.get('complemento'), 50) if data.get('complemento') else None,
            'cep': sanitize_input(data.get('cep'), 8) if data.get('cep') else None,
            'cidade': sanitize_input(data.get('cidade'), 50) if data.get('cidade') else None,
            'estado': sanitize_input(data.get('estado'), 2) if data.get('estado') else None,
            'updated_at': datetime.now(timezone.utc)
        }

        for key, value in update_fields.items():
            if value is not None:
                setattr(paciente, key, value)
        
        db.session.commit()
        user_ip = request.remote_addr
        user_timezone = get_user_timezone(user_ip)
        return jsonify({'message': 'Paciente atualizado com sucesso!', 'updated_at': get_local_time(paciente.updated_at, user_timezone).isoformat()}), 200

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500
@pacientes_routes.route('/api/excluir_paciente/<cpf>', methods=['DELETE'])
def excluir_paciente(cpf):
    """
    Exclui um paciente existente
    ---
    tags:
      - Pacientes
    parameters:
      - in: path
        name: cpf
        type: string
        required: true
        description: CPF do paciente
    responses:
      200:
        description: Paciente excluído com sucesso
      400:
        description: CPF inválido
      404:
        description: Paciente não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        paciente = Paciente.query.filter_by(cpf=cpf).first()
        if not paciente:
            raise NotFound("Paciente não encontrado")
        
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({'message': 'Paciente excluído com sucesso!'}), 200

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500