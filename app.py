from flask import Flask
from flask_cors import CORS
from db import db
from routes.user_routes import user_routes
from routes.pacientes_routes import pacientes_routes
from routes.convenios_routes import convenios_routes
from routes.acompanhamentos_routes import acompanhamentos_routes
from routes.auth_routes import auth_bp
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

CORS(app, resources=Config.CORS_RESOURCES)

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
app.register_blueprint(convenios_routes) 
app.register_blueprint(acompanhamentos_routes)
app.register_blueprint(auth_bp)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)