from flask import Flask, request, make_response
from flask_cors import CORS
from flasgger import Swagger
from src.infrastructure.database.db_config import init_db
from src.interfaces.api.routes.user_routes import user_routes
from src.interfaces.api.routes.auth_routes import auth_bp
from src.config.settings import Config
from src.config.container import init_container
from routes.pacientes_routes import pacientes_routes
from routes.convenios_routes import convenios_routes
from routes.acompanhamentos_routes import acompanhamentos_routes
from routes.planos_routes import planos_routes
from routes.cep_routes import cep_routes

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../cuidar-plus/cuidar-plus', static_folder='../cuidar-plus/cuidar-plus')
    app.config.from_object(config_class)
    
    # Inicializa o banco de dados
    init_db(app)
    
    # Inicializa o container
    init_container()
    
    # Configuração do Swagger
    app.config['SWAGGER'] = {
        'title': 'Cuidar+ API',
        'description': 'API para o sistema Cuidar+',
        'version': '1.0',
        'uiversion': 3,
        'specs_route': '/docs/'
    }
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

    # Registra as rotas
    app.register_blueprint(user_routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pacientes_routes)
    app.register_blueprint(convenios_routes)
    app.register_blueprint(acompanhamentos_routes)
    app.register_blueprint(planos_routes)
    app.register_blueprint(cep_routes, url_prefix='/api')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)