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
from flasgger import Swagger
from config import Config
from models.pacientes import Paciente
from models.acompanhamento import Acompanhamento
from models.user import User
from models.convenio import Convenio
from flask_migrate import Migrate

# Inicialização da aplicação
app = Flask(__name__, template_folder='../cuidar-plus/cuidar-plus', static_folder='../cuidar-plus/cuidar-plus')
app.config.from_object(Config)
swagger = Swagger(app)

# Configurar CORS para permitir apenas o domínio necessário
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,x-test-environment'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/api/options', methods=['OPTIONS'])
def options():
    return make_response('', 200)

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
app.register_blueprint(convenios_routes)
app.register_blueprint(acompanhamentos_routes)
app.register_blueprint(auth_bp)
app.register_blueprint(user_routes)
app.register_blueprint(planos_routes)
app.register_blueprint(cep_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)