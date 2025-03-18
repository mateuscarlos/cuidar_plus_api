from flask import Blueprint, request, jsonify
from models.user import User
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import Config

auth_bp = Blueprint('auth_bp', __name__)

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

        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(
            email=email, nome=nome, cpf=cpf, rua=rua, numero=numero, complemento=complemento,
            cep=cep, bairro=bairro, cidade=cidade, estado=estado, setor=setor, funcao=funcao,
            especialidade=especialidade, registro_categoria=registro_categoria, telefone=telefone,
            data_admissao=data_admissao, status=status, tipo_acesso=tipo_acesso, password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, Config.SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid email or password'}), 401