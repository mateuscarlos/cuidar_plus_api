from flask import Flask, Blueprint, request, jsonify
from models.user import User
from db import db
from flasgger import Swagger, swag_from
import re
import bleach
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from utils import validate_cpf, sanitize_input
import requests
from datetime import datetime

# Inicialização do Flask
app = Flask(__name__)

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

# Error handlers
@user_routes.errorhandler(BadRequest)
@user_routes.errorhandler(Conflict)
@user_routes.errorhandler(NotFound)
def handle_errors(e):
    return jsonify({
        'message': e.description,
        'error': type(e).__name__
    }), e.code

@user_routes.errorhandler(500)
def handle_internal_error(e):
    return jsonify({
        'message': 'Erro interno no servidor',
        'error': 'InternalServerError'
    }), 500

def camel_to_snake(data):
    """
    Converte as chaves de um dicionário de camelCase para snake_case.
    """
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
            new_data[new_key] = camel_to_snake(value) if isinstance(value, (dict, list)) else value
        return new_data
    elif isinstance(data, list):
        return [camel_to_snake(item) for item in data]
    else:
        return data

@user_routes.route('/usuarios/criar', methods=['POST'])
@swag_from({
    'tags': ['Usuários'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome': {'type': 'string', 'example': 'Maria Santos'},
                    'email': {'type': 'string', 'example': 'maria@email.com'},
                    'password_hash': {'type': 'string', 'example': 'senha_segura_hash'},
                    'cpf': {'type': 'string', 'example': '12345678901'},
                    'cep': {'type': 'string', 'example': '01001000'},
                    'setor': {'type': 'string', 'example': 'Enfermagem'},
                    'funcao': {'type': 'string', 'example': 'Enfermeira'},
                    'endereco': {
                        'type': 'object',
                        'properties': {
                            'numero': {'type': 'string', 'example': '123'},
                            'complemento': {'type': 'string', 'example': 'Apto 45'}
                        }
                    },
                    'telefone': {'type': 'string', 'example': '(11) 98765-4321'},
                    'especialidade': {'type': 'string', 'example': 'Clínica Geral'},
                    'registro_categoria': {'type': 'string', 'example': 'CRM-12345'},
                    'data_admissao': {'type': 'string', 'format': 'date', 'example': '2023-01-15'},
                    'tipo_acesso': {'type': 'string', 'example': 'Administrador'},
                    'tipo_contratacao': {'type': 'string', 'example': 'CLT'},
                    'status': {'type': 'string', 'example': 'Ativo'}
                },
                'required': ['nome', 'email', 'password_hash', 'cpf', 'cep']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Usuário criado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Usuário criado com sucesso'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'nome': {'type': 'string', 'example': 'Maria Santos'},
                            'email': {'type': 'string', 'example': 'maria@email.com'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Erro nos dados fornecidos',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Formato de data_admissao inválido. Use o formato ISO 8601.'}
                }
            }
        },
        '404': {
            'description': 'CEP não encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'CEP não encontrado'}
                }
            }
        },
        '500': {
            'description': 'Erro interno',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Erro ao criar usuário: mensagem de erro'}
                }
            }
        }
    }
})
def create_user():
    """
    Cria um novo usuário e consulta o endereço via API ViaCEP.
    """
    data = camel_to_snake(request.get_json())  # Converte camelCase para snake_case
    try:
        # Consulta o CEP na API ViaCEP
        cep = data.get('cep')
        if not cep:
            return jsonify({'error': 'CEP é obrigatório'}), 400

        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        response.raise_for_status()
        endereco_via_cep = response.json()

        if 'erro' in endereco_via_cep:
            return jsonify({'error': 'CEP não encontrado'}), 404

        # Mesclar o endereço da API ViaCEP com os dados enviados pelo formulário
        endereco_formulario = data.get('endereco', {})
        endereco_final = {
            # Dados do ViaCEP como referência
            'cep': cep,
            'logradouro': endereco_via_cep.get('logradouro', ''),
            'bairro': endereco_via_cep.get('bairro', ''),
            'localidade': endereco_via_cep.get('localidade', ''),
            'uf': endereco_via_cep.get('uf', ''),
            'estado': endereco_via_cep.get('uf', ''),
            
            # Sobrescrever com dados do formulário que têm prioridade
            'numero': endereco_formulario.get('numero', ''),
            'complemento': endereco_formulario.get('complemento', ''),
        }
        
        # Se houver mais campos no formulário, preservá-los
        if endereco_formulario:
            for key, value in endereco_formulario.items():
                if key not in ['cep'] and key not in endereco_final:
                    endereco_final[key] = value

        # Converte data_admissao para o formato correto (YYYY-MM-DD)
        data_admissao = data.get('data_admissao')
        if data_admissao:
            try:
                data_admissao = datetime.fromisoformat(data_admissao.replace("Z", "")).date()
            except ValueError:
                return jsonify({'error': 'Formato de data_admissao inválido. Use o formato ISO 8601.'}), 400

        # Converte tipo_contratacao para o formato aceito pelo banco
        tipo_contratacao = data.get('tipo_contratacao')
        if tipo_contratacao:
            if tipo_contratacao.lower() == 'contratada':
                tipo_contratacao = 'c'
            elif tipo_contratacao.lower() == 'terceirizada':
                tipo_contratacao = 't'
            elif tipo_contratacao.lower() == 'pessoa jurídica' :
                tipo_contratacao = 'p'

        # Cria o usuário
        user = User(
            nome=data.get('nome'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            cargo=data.get('cargo'),
            cpf=data.get('cpf'),
            cep=cep,
            setor=data.get('setor'),
            funcao=data.get('funcao'),
            endereco=endereco_final,  # Usando o endereço mesclado
            status=data.get('status'),
            telefone=data.get('telefone'),
            especialidade=data.get('especialidade'),
            registro_categoria=data.get('registro_categoria'),
            data_admissao=data_admissao,  # Valor convertido
            tipo_acesso=data.get('tipo_acesso'),
            tipo_contratacao=tipo_contratacao,  # Valor convertido
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Usuário criado com sucesso', 'user': user.to_dict()}), 201

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro ao consultar o serviço de CEP: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar usuário: {str(e)}'}), 500

@user_routes.route('/usuarios/lista', methods=['GET'])
@swag_from({
    'tags': ['Usuários'],
    'responses': {
        '200': {
            'description': 'Lista de usuários',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'nome': {'type': 'string', 'example': 'Maria Santos'},
                        'email': {'type': 'string', 'example': 'maria@email.com'},
                        'setor': {'type': 'string', 'example': 'Enfermagem'},
                        'funcao': {'type': 'string', 'example': 'Enfermeira'},
                        'status': {'type': 'string', 'example': 'Ativo'}
                    }
                }
            }
        },
        '500': {
            'description': 'Erro interno',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Erro ao listar usuários: mensagem de erro'}
                }
            }
        }
    }
})
def get_all_users():
    """
    Lista todos os usuários cadastrados.
    """
    try:
        usuarios = User.query.all()
        return jsonify([user.to_dict() for user in usuarios]), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao listar usuários: {str(e)}'}), 500


@user_routes.route('/usuarios/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Usuários'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        }
    ],
    'responses': {
        '200': {
            'description': 'Detalhes do usuário',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'nome': {'type': 'string', 'example': 'Maria Santos'},
                    'email': {'type': 'string', 'example': 'maria@email.com'},
                    'cpf': {'type': 'string', 'example': '12345678901'},
                    'setor': {'type': 'string', 'example': 'Enfermagem'},
                    'funcao': {'type': 'string', 'example': 'Enfermeira'},
                    'endereco': {
                        'type': 'object',
                        'properties': {
                            'cep': {'type': 'string', 'example': '01001000'},
                            'logradouro': {'type': 'string', 'example': 'Praça da Sé'},
                            'numero': {'type': 'string', 'example': '123'},
                            'complemento': {'type': 'string', 'example': 'Apto 45'},
                            'bairro': {'type': 'string', 'example': 'Sé'},
                            'localidade': {'type': 'string', 'example': 'São Paulo'},
                            'uf': {'type': 'string', 'example': 'SP'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Usuário não encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Erro ao buscar usuário: Usuário não encontrado'}
                }
            }
        },
        '500': {
            'description': 'Erro interno',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Erro ao buscar usuário: mensagem de erro'}
                }
            }
        }
    }
})
def get_user_by_id(id):
    """
    Retorna os detalhes de um usuário específico pelo ID.
    """
    try:
        user = User.query.get(id)
        if not user:
            raise NotFound('Usuário não encontrado')
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar usuário: {str(e)}'}), 500


@user_routes.route('/usuarios/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Usuários'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome': {'type': 'string', 'example': 'Maria Santos Atualizado'},
                    'email': {'type': 'string', 'example': 'maria_nova@email.com'},
                    'setor': {'type': 'string', 'example': 'Recepção'},
                    'funcao': {'type': 'string', 'example': 'Recepcionista'},
                    'cep': {'type': 'string', 'example': '02001000'},
                    'telefone': {'type': 'string', 'example': '(11) 98765-4321'},
                    'especialidade': {'type': 'string', 'example': 'Clínica Geral'},
                    'registro_categoria': {'type': 'string', 'example': 'CRM-12345'},
                    'tipo_acesso': {'type': 'string', 'example': 'Usuário'},
                    'tipo_contratacao': {'type': 'string', 'example': 'PJ'},
                    'status': {'type': 'string', 'example': 'Ativo'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Usuário atualizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Usuário atualizado com sucesso'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'nome': {'type': 'string', 'example': 'Maria Santos Atualizado'},
                            'email': {'type': 'string', 'example': 'maria_nova@email.com'}
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'Usuário não encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Usuário não encontrado'}
                }
            }
        },
        '500': {
            'description': 'Erro interno',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Erro ao atualizar usuário: mensagem de erro'}
                }
            }
        }
    }
})
def update_user(id):
    """
    Atualiza as informações de um usuário existente.
    """
    data = camel_to_snake(request.get_json())  # Converte camelCase para snake_case
    try:
        user = User.query.get(id)
        if not user:
            raise NotFound('Usuário não encontrado')

        # Atualiza o CEP e consulta o endereço via API ViaCEP
        new_cep = data.get('cep')
        if new_cep and new_cep != user.cep:
            try:
                response = requests.get(f'https://viacep.com.br/ws/{new_cep}/json/')
                response.raise_for_status()
                endereco_via_cep = response.json()

                if 'erro' in endereco_via_cep:
                    return jsonify({'error': 'CEP não encontrado'}), 404
                
                # Mesclar o endereço da API ViaCEP com os dados enviados pelo formulário
                endereco_formulario = data.get('endereco', {})
                endereco_final = {
                    # Dados do ViaCEP como referência
                    'cep': new_cep,
                    'logradouro': endereco_via_cep.get('logradouro', ''),
                    'bairro': endereco_via_cep.get('bairro', ''),
                    'localidade': endereco_via_cep.get('localidade', ''),
                    'uf': endereco_via_cep.get('uf', ''),
                    'estado': endereco_via_cep.get('uf', ''),
                    
                    # Sobrescrever com dados do formulário que têm prioridade
                    'numero': endereco_formulario.get('numero', ''),
                    'complemento': endereco_formulario.get('complemento', '')
                }
                
                # Se houver mais campos no formulário, preservá-los
                if endereco_formulario:
                    for key, value in endereco_formulario.items():
                        if key not in ['cep'] and key not in endereco_final:
                            endereco_final[key] = value

                user.cep = new_cep
                user.endereco = endereco_final
            except requests.exceptions.RequestException as e:
                return jsonify({'error': f'Erro ao consultar o serviço de CEP: {str(e)}'}), 500

        # Atualiza os campos permitidos
        user.nome = data.get('nome', user.nome)
        user.email = data.get('email', user.email)
        user.setor = data.get('setor', user.setor)
        user.funcao = data.get('funcao', user.funcao)
        user.telefone = data.get('telefone', user.telefone)
        user.especialidade = data.get('especialidade', user.especialidade)
        user.registro_categoria = data.get('registro_categoria', user.registro_categoria)
        user.tipo_acesso = data.get('tipo_acesso', user.tipo_acesso)
        user.tipo_contratacao = data.get('tipo_contratacao', user.tipo_contratacao)
        user.status = data.get('status', user.status)

        # Só atualizar o endereço se não foi alterado pelo CEP
        if 'endereco' in data and not new_cep:
            user.endereco = data.get('endereco')

        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso', 'user': user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar usuário: {str(e)}'}), 500

@user_routes.route('/usuarios/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Usuários'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário a ser excluído'
        }
    ],
    'responses': {
        '200': {
            'description': 'Usuário excluído com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Usuário excluído com sucesso'}
                }
            }
        },
        '404': {
            'description': 'Usuário não encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Usuário não encontrado'}
                }
            }
        },
        '500': {
            'description': 'Erro interno',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Erro ao excluir usuário: mensagem de erro'}
                }
            }
        }
    }
})
def delete_user(id):
    """
    Exclui logicamente um usuário (soft delete).
    """
    try:
        user = User.query.get(id)
        if not user:
            raise NotFound('Usuário não encontrado')

        # Marca o usuário como inativo
        user.status = 'Inativo'
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao excluir usuário: {str(e)}'}), 500

@user_routes.route('/usuarios/visualizar/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Usuários'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário'
        }
    ],
    'responses': {
        '200': {
            'description': 'Detalhes do usuário sem informações sensíveis',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'nome': {'type': 'string', 'example': 'Maria Santos'},
                    'email': {'type': 'string', 'example': 'maria@email.com'},
                    'cpf': {'type': 'string', 'example': '12345678901'},
                    'setor': {'type': 'string', 'example': 'Enfermagem'},
                    'funcao': {'type': 'string', 'example': 'Enfermeira'}
                }
            }
        },
        '404': {
            'description': 'Usuário não encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Usuário não encontrado'}
                }
            }
        },
        '500': {
            'description': 'Erro interno',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Erro ao buscar usuário: mensagem de erro'}
                }
            }
        }
    }
})
def visualizar_usuario(id):
    """
    Retorna os detalhes de um usuário específico pelo ID, excluindo o campo password_hash.
    """
    try:
        user = User.query.get(id)
        if not user:
            raise NotFound('Usuário não encontrado')

        # Converte o usuário para dicionário e remove o campo password_hash
        user_data = user.to_dict()
        user_data.pop('password_hash', None)

        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar usuário: {str(e)}'}), 500

# Adicione este novo endpoint de busca avançada para usuários

@user_routes.route('/usuarios/busca-avancada', methods=['GET'])
@swag_from({
    'tags': ['Usuários'],
    'parameters': [
        {
            'name': 'nome',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Nome completo ou parcial do usuário'
        },
        {
            'name': 'email',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Email do usuário'
        },
        {
            'name': 'cpf',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'CPF completo ou parcial do usuário'
        },
        {
            'name': 'id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'ID do usuário'
        },
        {
            'name': 'setor',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'ID ou nome do setor'
        },
        {
            'name': 'funcao',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'ID ou nome da função'
        },
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Status do usuário'
        },
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 1,
            'description': 'Página de resultados'
        },
        {
            'name': 'limit',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 10,
            'description': 'Quantidade de resultados por página'
        }
    ],
    'responses': {
        '200': {
            'description': 'Lista de usuários que correspondem aos critérios de busca',
            'schema': {
                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'nome': {'type': 'string', 'example': 'João Silva'},
                                'email': {'type': 'string', 'example': 'joao.silva@email.com'},
                                'cpf': {'type': 'string', 'example': '12345678901'},
                                'setor': {'type': 'string', 'example': 'Enfermagem'},
                                'funcao': {'type': 'string', 'example': 'Enfermeiro'},
                                'status': {'type': 'string', 'example': 'Ativo'}
                            }
                        }
                    },
                    'total': {'type': 'integer', 'example': 42},
                    'page': {'type': 'integer', 'example': 1},
                    'total_pages': {'type': 'integer', 'example': 5}
                }
            }
        },
        '400': {
            'description': 'Parâmetros inválidos',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'ID do usuário deve ser um número'}
                }
            }
        },
        '500': {
            'description': 'Erro interno',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Erro ao buscar usuários: mensagem de erro'}
                }
            }
        }
    }
})
def busca_avancada_usuarios():
    """
    Realiza busca avançada de usuários com múltiplos critérios.
    """
    try:
        # Extrair todos os parâmetros da query
        nome = request.args.get('nome', '')
        email = request.args.get('email', '')
        cpf = request.args.get('cpf', '')
        id_usuario = request.args.get('id', '')
        setor = request.args.get('setor', '')
        funcao = request.args.get('funcao', '')
        status = request.args.get('status', '')
        
        # Parâmetros de paginação
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
        except ValueError:
            return jsonify({'error': 'Parâmetros de paginação devem ser numéricos'}), 400
        
        # Iniciar a consulta
        query = User.query
        
        # Aplicar filtros somente se os parâmetros forem fornecidos
        if nome:
            query = query.filter(User.nome.ilike(f'%{nome}%'))
        
        if email:
            query = query.filter(User.email.ilike(f'%{email}%'))
        
        if cpf:
            query = query.filter(User.cpf.like(f'%{cpf}%'))
        
        if id_usuario:
            try:
                query = query.filter(User.id == int(id_usuario))
            except ValueError:
                return jsonify({'error': 'ID do usuário deve ser um número'}), 400
        
        if setor:
            # Tenta filtrar por ID do setor primeiro
            try:
                setor_id = int(setor)
                query = query.filter(User.setor == setor_id)
            except ValueError:
                # Se não for possível converter para int, filtra por nome do setor
                # Isso requer uma junção com a tabela de setores
                query = query.join(Setor, User.setor == Setor.id).filter(Setor.nome.ilike(f'%{setor}%'))
        
        if funcao:
            # Tenta filtrar por ID da função primeiro
            try:
                funcao_id = int(funcao)
                query = query.filter(User.funcao == funcao_id)
            except ValueError:
                # Se não for possível converter para int, filtra por nome da função
                query = query.join(Funcao, User.funcao == Funcao.id).filter(Funcao.nome.ilike(f'%{funcao}%'))
        
        if status:
            query = query.filter(User.status == status)
        
        # Ordenar os resultados por nome (pode ser customizado)
        query = query.order_by(User.nome)
        
        # Contar o total de resultados para a paginação
        total = query.count()
        
        # Aplicar a paginação
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        
        # Ajustar a página se estiver fora dos limites
        if page < 1:
            page = 1
        elif page > total_pages and total_pages > 0:
            page = total_pages
        
        # Aplicar offset e limit para paginação
        offset = (page - 1) * limit
        usuarios = query.offset(offset).limit(limit).all()
        
        # Converter para dicionário e remover senha
        resultado = []
        for u in usuarios:
            user_dict = u.to_dict()
            if 'password_hash' in user_dict:
                user_dict.pop('password_hash')
            resultado.append(user_dict)
        
        # Retornar resultado com informações de paginação
        response = {
            'items': resultado,
            'total': total,
            'page': page,
            'total_pages': total_pages
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': f"Erro ao buscar usuários: {str(e)}"}), 500

# Registrar o Blueprint no aplicativo
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)