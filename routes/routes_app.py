from flask import Blueprint
from .pacientes_routes import pacientes_routes
from .convenios_routes import convenios_routes
from .acompanhamentos_routes import acompanhamentos_routes
from .auth_routes import auth_bp
from .user_routes import user_routes

app_routes = Blueprint('app_routes', __name__)

def register_routes(app):
    # Registrar blueprints
    app.register_blueprint(pacientes_routes)
    app.register_blueprint(convenios_routes)
    app.register_blueprint(acompanhamentos_routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_routes)
    
    # Descomente as linhas abaixo se esses módulos estiverem implementados
    # from .tratamento.tratamentos_routes import tratamentos_routes
    # app.register_blueprint(tratamentos_routes)