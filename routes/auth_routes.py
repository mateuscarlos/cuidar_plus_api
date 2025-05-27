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
from config import Config  # Certifique-se de que o Config está importado

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

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para login de usuário
    """
    try:
        from argon2 import PasswordHasher
        from argon2.exceptions import VerifyMismatchError
        
        ph = PasswordHasher()
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'Dados não fornecidos'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email e senha são obrigatórios'}), 400
        
        # Buscar usuário por email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'message': 'Email ou senha inválidos'}), 401

        # Verificar a senha usando Argon2
        try:
            ph.verify(user.password_hash, password)
        except VerifyMismatchError:
            return jsonify({'message': 'Email ou senha inválidos'}), 401

        # Verificar se o usuário está ativo
        if user.status != 'ativo':
            return jsonify({'message': 'Usuário inativo. Contate o administrador'}), 401

        # Rehash da senha se necessário (para manter a segurança atualizada)
        if ph.check_needs_rehash(user.password_hash):
            user.password_hash = ph.hash(password)
            db.session.commit()

        # Gerar token JWT
        from datetime import datetime, timedelta
        import jwt
        
        expiration = datetime.utcnow() + timedelta(hours=24)
        payload = {
            'user_id': user.id,
            'email': user.email,
            'tipo_acesso': user.tipo_acesso,
            'exp': expiration,
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        # Salvar informações da sessão
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['logged_in'] = True

        # Log do login
        app.logger.info(f'Login realizado com sucesso para usuário {user.email} (ID: {user.id})')

        return jsonify({
            'message': 'Login realizado com sucesso',
            'token': token,
            'user': {
                'id': user.id,
                'nome': user.nome,
                'email': user.email,
                'setor': user.setor,
                'funcao': user.funcao,
                'tipo_acesso': user.tipo_acesso,
                'status': user.status
            }
        }), 200
        
    except Exception as e:
        app.logger.error(f'Erro no login: {str(e)}')
        return jsonify({'message': 'Erro interno do servidor'}), 500

@auth_bp.route('/api/protected-route', methods=['GET'])
def protected_route():
    """
    Exemplo de rota protegida que ignora a validação de token em modo de desenvolvimento.
    """
    if Config.ENV != 'development':  # Apenas verifica o token fora do modo de desenvolvimento
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token não fornecido'}), 401

        try:
            token = auth_header.split(" ")[1]
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

    return jsonify({'message': 'Acesso permitido (modo de desenvolvimento)'}), 200