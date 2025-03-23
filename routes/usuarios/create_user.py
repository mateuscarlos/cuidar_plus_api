from flask import Flask, Blueprint, request, jsonify
from models.user import User
from db import db
from flasgger import Swagger
import re
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from utils import validate_cpf, sanitize_input
from argon2 import PasswordHasher
from datetime import datetime

create_user_bp = Blueprint('create_user', __name__)
ph = PasswordHasher()  # Inicializa o objeto PasswordHasher

@create_user_bp.route('/api/criar_usuario', methods=['POST'])
def create_user():
    """
    Cria um novo usuário
    ---
    tags:
      - Usuários
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nome
            - cpf
            - setor
            - funcao
          properties:
            nome:
              type: string
              description: Nome do usuário
            cpf:
              type: string
              description: CPF do usuário
            rua:
              type: string
              description: Rua do usuário
            numero:
              type: string
              description: Número do endereço do usuário
            complemento:
              type: string
              description: Complemento do endereço do usuário
            cep:
              type: string
              description: CEP do usuário
            bairro:
              type: string
              description: Bairro do usuário
            cidade:
              type: string
              description: Cidade do usuário
            estado:
              type: string
              description: Estado do usuário
            setor:
              type: string
              description: Setor do usuário
            funcao:
              type: string
              description: Função do usuário
            especialidade:
              type: string
              description: Especialidade do usuário
            registro_categoria:
              type: string
              description: Registro da categoria do usuário
            email:
              type: string
              description: Email do usuário
            telefone:
              type: string
              description: Telefone do usuário
            data_admissao:
              type: string
              format: date
              description: Data de admissão do usuário
            status:
              type: string
              description: Status do usuário
            tipo_acesso:
              type: string
              description: Tipo de acesso do usuário
    responses:
      201:
        description: Usuário criado com sucesso
      400:
        description: Campos obrigatórios faltando ou CPF inválido
      409:
        description: CPF já cadastrado
      500:
        description: Erro interno no servidor
    """
    try:
        data = request.get_json()
        required_fields = ['nome', 'cpf', 'setor', 'funcao']
        if not all(field in data for field in required_fields):
            raise BadRequest("Campos obrigatórios faltando: nome, cpf, setor, funcao")
        
        cpf = sanitize_input(data['cpf'], 11)
        cpf = re.sub(r'[^\d]', '', cpf)
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        if User.query.filter_by(cpf=cpf).first():
            raise Conflict("CPF já cadastrado")

        # Se uma senha for fornecida, faça o hash usando Argon2
        password = data.get('password')
        password_hash = ph.hash(password) if password else None

        # Format the data_admissao to 'YYYY-MM-DD'
        data_admissao = data.get('data_admissao')
        if data_admissao:
            try:
                data_admissao = datetime.strptime(data_admissao, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                raise BadRequest("Formato de data inválido. Por favor, utilize o formato DD/MM/YYYY.")

        user_data = {
            'nome': sanitize_input(data['nome'], 100),
            'cpf': cpf,
            'rua': sanitize_input(data.get('rua'), 100) if data.get('rua') else None,
            'numero': sanitize_input(data.get('numero'), 10) if data.get('numero') else None,
            'complemento': sanitize_input(data.get('complemento'), 50) if data.get('complemento') else None,
            'cep': sanitize_input(data.get('cep'), 8) if data.get('cep') else None,
            'bairro': sanitize_input(data.get('bairro'), 50) if data.get('bairro') else None,
            'cidade': sanitize_input(data.get('cidade'), 50) if data.get('cidade') else None,
            'estado': sanitize_input(data.get('estado'), 2) if data.get('estado') else None,
            'setor': sanitize_input(data['setor'], 50),
            'funcao': sanitize_input(data['funcao'], 50),
            'email': sanitize_input(data.get('email'), 100) if data.get('email') else None,
            'telefone': sanitize_input(data.get('telefone'), 20) if data.get('telefone') else None,
            'data_admissao': data_admissao,
            'status': sanitize_input(data.get('status'), 20) if data.get('status') else 'Ativo',
            'tipo_acesso': sanitize_input(data.get('tipo_acesso'), 20) if data.get('tipo_acesso') else None,
            'especialidade': sanitize_input(data.get('especialidade'), 50) if data.get('especialidade') else None,
            'registro_categoria': sanitize_input(data.get('registro_categoria'), 20) if data.get('registro_categoria') else None
        }
        
        # Adicionar o hash da senha apenas se uma senha foi fornecida
        if password_hash:
            user_data['password_hash'] = password_hash

        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Usuário criado com sucesso', 'id': new_user.id}), 201

    except BadRequest as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except Conflict as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno no servidor: {str(e)}'}), 500