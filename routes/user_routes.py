from flask import Flask, Blueprint, request, jsonify
from models.user import User
from db import db
from flasgger import Swagger, swag_from
import re
import bleach
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

# Inicialização do Flask
app = Flask(__name__)

# Configurações de segurança
talisman = Talisman(app)
limiter = Limiter(app=app, key_func=get_remote_address)

# Configuração do Flasgger (Swagger)
app.config['SWAGGER'] = {
    'title': 'API de Usuários',
    'description': 'API para gerenciamento de usuários',
    'version': '1.0',
    'uiversion': 3,
    'specs_route': '/docs/'  # Rota para acessar a documentação Swagger
}
swagger = Swagger(app)

# Blueprint para as rotas de usuário
user_routes = Blueprint('user_routes', __name__)

def validate_cpf(cpf: str) -> bool:
    """Valida o formato e dígitos verificadores do CPF"""
    cpf = re.sub(r'[^\d]', '', cpf)
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito1 = resto if resto < 10 else 0
    
    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito2 = resto if resto < 10 else 0
    
    return cpf[-2:] == f"{digito1}{digito2}"

def sanitize_input(value: str, max_length=100) -> str:
    """Sanitiza e valida entradas de texto"""
    if not value:
        return value
    cleaned = bleach.clean(value.strip())
    if len(cleaned) > max_length:
        raise ValueError(f"Campo excede o tamanho máximo de {max_length} caracteres")
    return cleaned

@user_routes.route('/api/criar_usuario', methods=['POST'])
@swag_from('swagger/create_user.yml')
@limiter.limit("10/minute")
def create_user():
    """
    Cria um novo usuário.

    Valida os campos obrigatórios, verifica se o CPF é válido e se já existe no banco de dados.
    Sanitiza e valida as entradas de texto.
    Cria um novo objeto User com as informações recebidas e salva no banco de dados.

    Retorna:
        201 - Usuário criado com sucesso, com a matrícula do novo usuário.
        400 - Erro de validação de entrada (campos obrigatórios faltando ou CPF inválido).
        409 - CPF já cadastrado.
        500 - Erro interno no servidor.
    """

    try:
        data = request.get_json()
        
        # Validação dos campos obrigatórios
        required_fields = ['nome', 'cpf', 'setor', 'funcao']
        if not all(field in data for field in required_fields):
            raise BadRequest("Campos obrigatórios faltando: nome, cpf, setor, funcao")
        
        # Sanitização e validação
        cpf = re.sub(r'[^\d]', '', data['cpf'])
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        if User.query.filter_by(cpf=cpf).first():
            raise Conflict("CPF já cadastrado")

        user_data = {
            'nome': sanitize_input(data['nome'], 100),
            'cpf': cpf,
            'endereco': sanitize_input(data.get('endereco'), 200),
            'setor': sanitize_input(data['setor'], 50),
            'funcao': sanitize_input(data['funcao'], 50),
            'especialidade': sanitize_input(data.get('especialidade'), 50),
            'registro_categoria': sanitize_input(data.get('registro_categoria'), 20)
        }

        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': 'Usuário criado com sucesso!',
            'matricula': new_user.id
        }), 201

    except ValueError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno no servidor'}), 500

@user_routes.route('/api/exibe_usuarios', methods=['GET'])
@swag_from('swagger/get_users.yml')
@limiter.limit("60/minute")
def get_all_users():
    """
    Recupera todos os usuários do banco de dados, com opção de filtrar por setor.

    Parâmetros:
        page (int): Número da página a ser recuperada (padrão: 1)
        per_page (int): Número de usuários por página (padrão: 10)
        setor (str): Setor para filtrar os usuários (opcional)

    Retorna:
        200 - Lista de usuários com informações básicas e metadados de paginação.
        500 - Erro interno no servidor.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = User.query
        if setor := request.args.get('setor'):
            query = query.filter_by(setor=sanitize_input(setor))
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'usuarios': [{
                'matricula': u.id,
                'nome': u.nome,
                'setor': u.setor,
                'funcao': u.funcao,
                'cpf': u.cpf
            } for u in pagination.items],
            'total': pagination.total,
            'paginas': pagination.pages,
            'pagina_atual': page
        }), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao recuperar usuários'}), 500

@user_routes.route('/api/atualizar_usuario/<cpf>', methods=['PUT'])
@swag_from('swagger/update_user.yml')
@limiter.limit("30/minute")
def atualizar_usuario(cpf):
    """
    Atualiza as informações de um usuário existente no banco de dados.

    Esta função recebe um CPF como parâmetro e atualiza os campos do
    usuário correspondente no banco de dados com os dados fornecidos
    na requisição. Valida o CPF, sanitiza as entradas e garante que
    apenas os campos fornecidos sejam atualizados.

    Parâmetros:
        cpf (str): CPF do usuário a ser atualizado.

    Retorna:
        200 - Mensagem de sucesso se o usuário for atualizado corretamente.
        400 - Mensagem de erro se ocorrer algum problema na atualização.
    """

    try:
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        usuario = User.query.filter_by(cpf=cpf).first()
        if not usuario:
            raise NotFound("Usuário não encontrado")

        data = request.get_json()
        update_fields = {
            'nome': sanitize_input(data.get('nome'), 100),
            'setor': sanitize_input(data.get('setor'), 50),
            'funcao': sanitize_input(data.get('funcao'), 50),
            'especialidade': sanitize_input(data.get('especialidade'), 50),
            'registro_categoria': sanitize_input(data.get('registro_categoria'), 20)
        }

        for key, value in update_fields.items():
            if value is not None:
                setattr(usuario, key, value)
        
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@user_routes.route('/api/excluir_usuario/<cpf>', methods=['DELETE'])
@swag_from('swagger/delete_user.yml')
@limiter.limit("30/minute")
def excluir_usuario(cpf):
    """
    Exclui um usuário.

    Parâmetros:
        cpf (str): CPF do usuário a ser excluído.

    Retorna:
        200 - Mensagem de sucesso se o usuário for excluído corretamente.
        400 - Mensagem de erro se ocorrer algum problema na exclusão.
    """
    try:
        if not validate_cpf(cpf):
            raise BadRequest("CPF inválido")
            
        usuario = User.query.filter_by(cpf=cpf).first()
        if not usuario:
            raise NotFound("Usuário não encontrado")
        
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

# Error handlers
@user_routes.errorhandler(BadRequest)
@user_routes.errorhandler(Conflict)
@user_routes.errorhandler(NotFound)
def handle_errors(e):
    """
    Função de tratamento de erros para requests mal formatadas.

    Retorna uma resposta JSON com o código de status 400, 409 ou 404,
    dependendo do tipo de erro, com uma chave 'message' contendo a
    descrição do erro e uma chave 'error' com o nome do tipo de erro.

    Parâmetros:
        e (Exception): Instância da exceção que originou o erro.

    Retorna:
        400 - BadRequest
        409 - Conflict
        404 - NotFound
    """
    return jsonify({
        'message': e.description,
        'error': type(e).__name__
    }), e.code

@user_routes.errorhandler(500)
def handle_internal_error(e):
    """
    Handles internal server errors.

    This function is triggered when an unhandled exception
    occurs in the application, resulting in an HTTP 500 error.
    It returns a JSON response with a message indicating an
    internal server error and includes the error type.

    Parameters:
        e (Exception): The exception instance that caused the error.

    Returns:
        JSON response with HTTP status code 500.
    """

    return jsonify({
        'message': 'Erro interno no servidor',
        'error': 'InternalServerError'
    }), 500

# Registrar o Blueprint no aplicativo
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)