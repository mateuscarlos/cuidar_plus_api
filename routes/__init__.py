from .pacientes.pacientes_app import pacientes_routes
from .tratamento.tratamentos_routes import tratamentos_routes
from .convenios.convenios_routes import convenios_routes
from .auth_routes import auth_bp

__all__ = [
    'pacientes_routes',
    'tratamentos_routes',
    'convenios_routes',
    'auth_bp'
]