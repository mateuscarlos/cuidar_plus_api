from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from models.user import User
from db import db
import datetime
import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

auth_bp = Blueprint('auth', __name__)
ph = PasswordHasher()  # Inicializa o objeto PasswordHasher da biblioteca argon2-cffi

@auth_bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        password = data.get('password')
        email = data.get('email')
        nome = data.get('nome')
        cpf = data.get('cpf')
        rua = data.get('rua')
        numero = data.get('numero')
        complemento = data.get('complemento')
        cep = data.get('cep')
        bairro = data.get('bairro')
        cidade = data.get('cidade')
        estado = data.get('estado')
        setor = data.get('setor')
        funcao = data.get('funcao')
        especialidade = data.get('especialidade')
        registro_categoria = data.get('registro_categoria')
        telefone = data.get('telefone')
        data_admissao = data.get('data_admissao')
        status = data.get('status')
        tipo_acesso = data.get('tipo_acesso')

        # Convertendo a data_admissao para o formato YYYY-MM-DD
        data_admissao = datetime.datetime.strptime(data_admissao, '%d%m%Y').strftime('%Y-%m-%d')

        if User.query.filter_by(email=email).first() or User.query.filter_by(cpf=cpf).first():
            return jsonify({'message': 'Email or CPF already exists'}), 409

        # Usando Argon2 para criar hash da senha de maneira mais segura
        hashed_password = ph.hash(password)

        new_user = User(
            email=email, nome=nome, cpf=cpf, rua=rua, numero=numero, complemento=complemento,
            cep=cep, bairro=bairro, cidade=cidade, estado=estado, setor=setor, funcao=funcao,
            especialidade=especialidade, registro_categoria=registro_categoria, telefone=telefone,
            data_admissao=data_admissao, status=status, tipo_acesso=tipo_acesso, password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return jsonify({'message': 'Invalid email or password'}), 401
        try:
            # Verifica a senha usando Argon2
            ph.verify(user.password_hash, data.get('password'))
            # Se a senha precisa ser rehashed (devido a mudanças nos parâmetros de segurança)
            if ph.check_needs_rehash(user.password_hash):
                user.password_hash = ph.hash(data.get('password'))
                db.session.commit()
                
            # Gerando o token JWT
            expiration = datetime.utcnow() + timedelta(hours=24)
            payload = {
                'user_id': user.id,
                'exp': expiration
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
                
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'nome': user.nome,
                    'email': user.email,
                    'cargo': user.cargo,
                    'permissions': user.permissions
                },
                'token': token
            }), 200
        except VerifyMismatchError:
            return jsonify({'message': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'message': f'Login error: {str(e)}'}), 500