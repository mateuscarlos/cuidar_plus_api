from flask import Blueprint, request, jsonify
from models.user import User
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from utils import validate_cpf
from sqlalchemy import or_

get_users_bp = Blueprint('get_users', __name__)

@get_users_bp.route('/api/usuarios', methods=['GET'])
def get_all_users():
    """
    Exibe todos os usuários
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários
      500:
        description: Erro ao recuperar usuários
    """
    try:
        # Busca todos os usuários sem paginação
        usuarios = User.query.all()

        # Retorna a lista de usuários sem senha
        usuarios_sem_senha = [
            {
                'id': usuario.id,
                'email': usuario.email,
                'nome': usuario.nome,
                'cpf': usuario.cpf,
                'rua': usuario.rua,
                'numero': usuario.numero,
                'complemento': usuario.complemento,
                'cep': usuario.cep,
                'bairro': usuario.bairro,
                'cidade': usuario.cidade,
                'estado': usuario.estado,
                'setor': usuario.setor,
                'funcao': usuario.funcao,
                'especialidade': usuario.especialidade,
                'registro_categoria': usuario.registro_categoria,
                'telefone': usuario.telefone,
                'data_admissao': usuario.data_admissao,
                'status': usuario.status,
                'tipo_acesso': usuario.tipo_acesso
            }
            for usuario in usuarios
        ]
        return jsonify({'usuarios': usuarios_sem_senha}), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao recuperar usuários', 'error': str(e)}), 500


@get_users_bp.route('/api/usuario/<int:id>', methods=['GET'])
def get_usuario_by_id(id):
    """
    Obtém os dados de um usuário pelo ID
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Dados do usuário
      400:
        description: ID inválido
      404:
        description: Usuário não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        if not str(id).isdigit():
            raise BadRequest("ID inválido")
            
        usuario = User.query.filter_by(id=id).first()
        if not usuario:
            raise NotFound("Usuário não encontrado")

        return jsonify({
            'usuario': {
                'id': usuario.id,
                'nome': usuario.nome,
                'cpf': usuario.cpf,
                'rua': usuario.rua,
                'numero': usuario.numero,
                'complemento': usuario.complemento,
                'cep': usuario.cep,
                'bairro': usuario.bairro,
                'cidade': usuario.cidade,
                'estado': usuario.estado,
                'setor': usuario.setor,
                'funcao': usuario.funcao,
                'especialidade': usuario.especialidade,
                'registro_categoria': usuario.registro_categoria,
                'email': usuario.email,
                'telefone': usuario.telefone,
                'data_admissao': usuario.data_admissao,
                'status': usuario.status,
                'tipo_acesso': usuario.tipo_acesso
            }
        }), 200

    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500


@get_users_bp.route('/api/usuario/cpf/<string:cpf>', methods=['GET'])
def get_usuario_by_cpf(cpf):
    """
    Obtém os dados de usuário(s) pelo CPF (parcial ou completo)
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: cpf
        type: string
        required: true
        description: CPF do usuário (completo ou parcial, mínimo 3 dígitos)
    responses:
      200:
        description: Lista de usuários encontrados ou dados de um único usuário
      400:
        description: CPF inválido ou muito curto
      404:
        description: Usuário não encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        # Verifica se tem pelo menos 3 caracteres para busca
        if len(cpf) < 3:
            raise BadRequest("É necessário informar pelo menos 3 dígitos para a busca")
            
        # Se for um CPF completo (11 dígitos), valida e busca exato
        if len(cpf) == 11 and cpf.isdigit():
            if not validate_cpf(cpf):
                raise BadRequest("CPF inválido")
                
            usuario = User.query.filter_by(cpf=cpf).first()
            if not usuario:
                raise NotFound("Usuário não encontrado")

            # Retorna os dados completos do usuário
            return jsonify({
                'usuario': {
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'cpf': usuario.cpf,
                    'rua': usuario.rua,
                    'numero': usuario.numero,
                    'complemento': usuario.complemento,
                    'cep': usuario.cep,
                    'bairro': usuario.bairro,
                    'cidade': usuario.cidade,
                    'estado': usuario.estado,
                    'setor': usuario.setor,
                    'funcao': usuario.funcao,
                    'especialidade': usuario.especialidade,
                    'registro_categoria': usuario.registro_categoria,
                    'email': usuario.email,
                    'telefone': usuario.telefone,
                    'data_admissao': usuario.data_admissao.strftime('%Y-%m-%d') if usuario.data_admissao else None,
                    'status': usuario.status,
                    'tipo_acesso': usuario.tipo_acesso,
                    'created_at': usuario.created_at.strftime('%Y-%m-%d %H:%M:%S') if usuario.created_at else None,
                    'updated_at': usuario.updated_at.strftime('%Y-%m-%d %H:%M:%S') if usuario.updated_at else None
                }
            }), 200
        
        # Caso contrário, faz busca parcial
        termo_busca = f"%{cpf}%"
        usuarios = User.query.filter(User.cpf.like(termo_busca)).all()
        
        if not usuarios:
            return jsonify({
                'message': 'Nenhum usuário encontrado com o CPF informado',
                'usuarios': []
            }), 404
        
        # Prepara resposta com lista resumida de usuários
        resultado = []
        for usuario in usuarios:
            resultado.append({
                'id': usuario.id,
                'nome': usuario.nome,
                'cpf': usuario.cpf,
                'email': usuario.email,
                'telefone': usuario.telefone,
                'setor': usuario.setor,
                'funcao': usuario.funcao,
                'especialidade': usuario.especialidade,
                'status': usuario.status,
                'tipo_acesso': usuario.tipo_acesso
            })
        
        return jsonify({
            'total': len(resultado),
            'usuarios': resultado
        }), 200

    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except NotFound as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500


@get_users_bp.route('/api/usuario/nome', methods=['GET'])
def get_usuario_by_name():
    """
    Busca usuários pelo nome ou parte do nome
    ---
    tags:
      - Usuários
    parameters:
      - in: query
        name: nome
        type: string
        required: true
        description: Nome ou parte do nome do usuário para busca
    responses:
      200:
        description: Lista de usuários encontrados
      400:
        description: Parâmetro de busca inválido
      404:
        description: Nenhum usuário encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        # Obtém o parâmetro de busca
        nome_busca = request.args.get('nome', '')
        
        # Valida o parâmetro de busca
        if not nome_busca or len(nome_busca) < 3:
            raise BadRequest("É necessário informar pelo menos 3 caracteres para a busca")
        
        # Realiza a busca com LIKE para encontrar nomes parciais (case insensitive)
        termo_busca = f"%{nome_busca}%"
        usuarios = User.query.filter(User.nome.ilike(termo_busca)).all()
        
        # Verifica se encontrou algum resultado
        if not usuarios:
            return jsonify({
                'message': 'Nenhum usuário encontrado com o termo informado',
                'usuarios': []
            }), 404
        
        # Prepara a resposta com os usuários encontrados
        resultado = []
        for usuario in usuarios:
            resultado.append({
                'id': usuario.id,
                'nome': usuario.nome,
                'cpf': usuario.cpf,
                'email': usuario.email,
                'telefone': usuario.telefone,
                'setor': usuario.setor,
                'funcao': usuario.funcao,
                'especialidade': usuario.especialidade,
                'status': usuario.status,
                'tipo_acesso': usuario.tipo_acesso
            })
        
        return jsonify({
            'total': len(resultado),
            'usuarios': resultado
        }), 200

    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500


@get_users_bp.route('/api/usuarios/buscar', methods=['GET'])
def buscar_usuarios():
    """
    Busca genérica de usuários por campo específico
    ---
    tags:
      - Usuários
    parameters:
      - in: query
        name: campo
        type: string
        required: true
        description: Campo para busca (id, nome, cpf)
      - in: query
        name: valor
        type: string
        required: true
        description: Valor a ser buscado
    responses:
      200:
        description: Lista de usuários encontrados
      400:
        description: Parâmetros de busca inválidos
      404:
        description: Nenhum usuário encontrado
      500:
        description: Erro interno no servidor
    """
    try:
        # Obtém os parâmetros da busca
        campo = request.args.get('campo')
        valor = request.args.get('valor')

        # Valida os parâmetros
        if not campo or not valor:
            raise BadRequest("Campo e valor são obrigatórios")

        if len(valor) < 2:
            raise BadRequest("É necessário informar pelo menos 3 caracteres para a busca")

        # Define os campos permitidos para busca
        campos_permitidos = {
            'id': User.id,
            'nome': User.nome,
            'cpf': User.cpf,
            'email': User.email
        }

        if campo not in campos_permitidos:
            raise BadRequest(f"Campo de busca inválido. Campos permitidos: {', '.join(campos_permitidos.keys())}")

        # Prepara a query base
        query = User.query

        # Aplica o filtro adequado conforme o campo
        if campo == 'id':
            if not valor.isdigit():
                raise BadRequest("O valor deve ser numérico para busca por ID")
            query = query.filter(User.id == int(valor))
        elif campo == 'cpf':
            query = query.filter(User.cpf.like(f"%{valor}%"))
        else:
            # Para outros campos, usa busca case-insensitive com LIKE
            query = query.filter(campos_permitidos[campo].ilike(f"%{valor}%"))

        # Executa a busca
        usuarios = query.all()

        if not usuarios:
            return jsonify({
                'message': 'Nenhum usuário encontrado',
                'usuarios': []
            }), 404

        # Prepara o resultado
        resultado = []
        for usuario in usuarios:
            resultado.append({
                'id': usuario.id,
                'nome_completo': usuario.nome,
                'cpf': usuario.cpf,
                'email': usuario.email,
                'telefone': usuario.telefone,
                'cargo': usuario.funcao,
                'setor': usuario.setor,
                'status': usuario.status
            })

        return jsonify({
            'total': len(resultado),
            'usuarios': resultado
        }), 200

    except BadRequest as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Erro interno no servidor', 'error': str(e)}), 500