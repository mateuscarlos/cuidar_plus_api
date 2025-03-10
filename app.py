from flask import Flask
from flask_cors import CORS
from db import db
from routes.user_routes import user_routes
from routes.routes_app import app_routes
from routes.pacientes.pacientes_app import pacientes_routes
from flasgger import Swagger
from config import Config
from models.pacientes import Paciente
from flask_migrate import Migrate

app = Flask(__name__, template_folder='../cuidar-plus/cuidar-plus', static_folder='../cuidar-plus/cuidar-plus')
app.config.from_object(Config)
swagger = Swagger(app)

CORS(app, resources=Config.CORS_RESOURCES)

db.init_app(app)
migrate = Migrate(app, db)  # Adicione esta linha para configurar Flask-Migrate

with app.app_context():
    try:
        db.create_all()
        print("Banco de dados criado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

# Registro de rotas
app.register_blueprint(app_routes)
app.register_blueprint(user_routes)
app.register_blueprint(pacientes_routes)  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)