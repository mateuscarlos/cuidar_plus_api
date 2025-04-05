from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from db import db
from routes.user_routes import user_routes
from routes.pacientes_routes import pacientes_routes
from routes.convenio_plano_routes import convenio_plano_routes  # Importação do blueprint unificado
from routes.acompanhamentos_routes import acompanhamentos_routes
from routes.auth_routes import auth_bp
from routes.cep_routes import cep_routes
from routes.debug_routes import debug_routes
from flasgger import Swagger
from config import Config
from models.pacientes import Paciente
from models.acompanhamento import Acompanhamento
from models.user import User
from models.convenio import Convenio
from models.plano import Plano  # Adicionando import do modelo Plano
from flask_migrate import Migrate

# Inicialização da aplicação
app = Flask(__name__, template_folder='../cuidar-plus/cuidar-plus', static_folder='../cuidar-plus/cuidar-plus')
app.config.from_object(Config)
swagger = Swagger(app)

# Configurar CORS para permitir o cabeçalho 'x-test-environment'
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,x-test-environment')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/api/options', methods=['OPTIONS'])
def options():
    return make_response('', 200)

# Adicionar rota de depuração para verificar se o serviço está online
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok', 'message': 'API is running'}), 200

# Inicialização do banco de dados
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    try:
        db.create_all()
        print("Banco de dados criado com sucesso.")
        
        # Verificar tabelas criadas
        tables = ['paciente', 'acompanhamento', 'convenio', 'plano']
        for table in tables:
            if table in db.metadata.tables:
                print(f"Tabela '{table}' criada com sucesso.")
            else:
                print(f"Tabela '{table}' não foi criada.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

# Registro de rotas
app.register_blueprint(pacientes_routes)

app.register_blueprint(convenio_plano_routes)  # Registro do novo blueprint unificado
app.register_blueprint(acompanhamentos_routes)
app.register_blueprint(auth_bp)
app.register_blueprint(user_routes)
app.register_blueprint(cep_routes, url_prefix='/api')
app.register_blueprint(debug_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)