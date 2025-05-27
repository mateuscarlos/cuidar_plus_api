from flask import Flask, request, make_response
from flask_cors import CORS
from db import db
from routes.user_routes import user_routes
from routes.pacientes_routes import pacientes_routes
from routes.convenios_routes import convenios_routes
from routes.acompanhamentos_routes import acompanhamentos_routes
from routes.auth_routes import auth_bp
from routes.planos_routes import planos_routes
from routes.cep_routes import cep_routes
from routes.routes_setor import setor_bp
from routes.routes_funcoes import funcao_bp
from flasgger import Swagger
from config import Config

from flask_migrate import Migrate

# Inicialização da aplicação
app = Flask(__name__, template_folder='../cuidar-plus/cuidar-plus', static_folder='../cuidar-plus/cuidar-plus')
app.config.from_object(Config)

# Configurar CORS
CORS(app, resources=Config.CORS_RESOURCES, supports_credentials=True)

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Cuidar+ API",
        "description": "API para gerenciamento do sistema Cuidar+",
        "version": "1.0.0",
        "contact": {
            "name": "Equipe de Desenvolvimento",
            "email": "dev@cuidar.com"
        }
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header usando o esquema Bearer. Exemplo: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ],
    "tags": [
        {
            "name": "Autenticação",
            "description": "Endpoints de autenticação e gerenciamento de tokens"
        },
        {
            "name": "Usuários",
            "description": "Gerenciamento de usuários do sistema"
        },
        {
            "name": "Pacientes",
            "description": "Cadastro e gerenciamento de pacientes"
        },
        {
            "name": "Acompanhamentos",
            "description": "Registros de acompanhamentos médicos"
        },
        {
            "name": "Convênios",
            "description": "Gerenciamento de convênios médicos"
        },
        {
            "name": "Setores",
            "description": "Gerenciamento de setores da instituição"
        },
        {
            "name": "Funções",
            "description": "Gerenciamento de funções por setor"
        },
        {
            "name": "Dicionários",
            "description": "Endpoints que retornam dados no formato de dicionários"
        }
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin in Config.CORS_RESOURCES[r"/*"]["origins"]:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,x-test-environment'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/api/options', methods=['OPTIONS'])
def options():
    return make_response('', 200)

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'ok'}, 200

# Inicialização do banco de dados
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    try:
        db.create_all()
        print("Banco de dados criado com sucesso.")
        
        # Verificar tabelas criadas no banco de dados
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        tables = ['paciente', 'acompanhamento', 'convenio', 'plano', 'user']
        for table in tables:
            if table in existing_tables:
                print(f"Tabela '{table}' criada com sucesso.")
            else:
                print(f"Tabela '{table}' não foi criada.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

# Registro de rotas
app.register_blueprint(pacientes_routes)
app.register_blueprint(user_routes)
app.register_blueprint(auth_bp)
app.register_blueprint(convenios_routes)
app.register_blueprint(acompanhamentos_routes)
app.register_blueprint(planos_routes)
app.register_blueprint(cep_routes)
app.register_blueprint(setor_bp)
app.register_blueprint(funcao_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)