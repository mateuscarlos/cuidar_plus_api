from flask import Blueprint, request, jsonify, current_app as app
from werkzeug.security import check_password_hash
from models.user import User
from db import db
import datetime
import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)
ph = PasswordHasher()  # Inicializa o objeto PasswordHasher da biblioteca argon2-cffi

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """
    Rota para registrar um novo usuário.
    """
    try:
        data = request.get_json()

        # Validação de campos obrigatórios
        required_fields = ['nome', 'email', 'password', 'cpf', 'setor', 'funcao', 'cep']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'O campo {field} é obrigatório'}), 400

        # Validação de CPF
        if not validate_cpf(data['cpf']):
            return jsonify({'message': 'CPF inválido'}), 400

        # Verificar duplicidade de email ou CPF
        if User.query.filter((User.email == data['email']) | (User.cpf == data['cpf'])).first():
            return jsonify({'message': 'Email ou CPF já cadastrado'}), 409

        # Hash da senha
        hashed_password = ph.hash(data['password'])

        # Consulta o CEP na API ViaCEP
        response = requests.get(f'https://viacep.com.br/ws/{data["cep"]}/json/')
        response.raise_for_status()
        endereco_data = response.json()

        if 'erro' in endereco_data:
            return jsonify({'message': 'CEP não encontrado'}), 404

        # Criar novo usuário
        new_user = User(
            nome=data['nome'],
            email=data['email'],
            password_hash=hashed_password,
            cpf=data['cpf'],
            setor=data['setor'],
            funcao=data['funcao'],
            endereco=endereco_data,  # Salva o endereço como JSON
            status='Ativo',  # Status padrão
            tipo_acesso=data.get('tipo_acesso', 'Usuário')  # Tipo de acesso padrão
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Usuário registrado com sucesso', 'user': new_user.to_dict()}), 201

    except requests.exceptions.RequestException as e:
        return jsonify({'message': f'Erro ao consultar o serviço de CEP: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao registrar usuário: {str(e)}'}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """
    Rota para autenticar um usuário.
    """
    try:
        data = request.get_json()

        # Buscar usuário pelo email
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return jsonify({'message': 'Email ou senha inválidos'}), 401

        # Verificar a senha usando Argon2
        try:
            ph.verify(user.password_hash, data.get('password'))
        except VerifyMismatchError:
            return jsonify({'message': 'Email ou senha inválidos'}), 401

        # Rehash da senha, se necessário
        if ph.check_needs_rehash(user.password_hash):
            user.password_hash = ph.hash(data.get('password'))
            db.session.commit()

        # Gerar token JWT
        expiration = datetime.utcnow() + timedelta(hours=24)
        payload = {
            'user_id': user.id,
            'exp': expiration
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': {
                'id': user.id,
                'nome': user.nome,
                'email': user.email,
                'setor': user.setor,
                'funcao': user.funcao,
                'status': user.status
            },
            'token': token
        }), 200

    except Exception as e:
        return jsonify({'message': f'Erro ao realizar login: {str(e)}'}), 500