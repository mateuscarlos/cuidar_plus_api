from .pacientes_routes import pacientes_routes
from .convenios_routes import convenios_routes
from .acompanhamentos_routes import acompanhamentos_routes
from .auth_routes import auth_bp
from .user_routes import user_routes
from .routes_setor import setor_bp
from .routes_funcoes import funcao_bp

__all__ = [
    'pacientes_routes',
    'convenios_routes',
    'acompanhamentos_routes',
    'auth_bp',
    'user_routes',
    'setor_bp',
    'funcao_bp'
]