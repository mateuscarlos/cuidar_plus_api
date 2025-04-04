# Importações para o pacote routes
from .pacientes_routes import pacientes_routes
from .convenio_plano_routes import convenio_plano_routes  # Atualizado para usar o módulo unificado
from .acompanhamentos_routes import acompanhamentos_routes
from .auth_routes import auth_bp
from .user_routes import user_routes
from .cep_routes import cep_routes
from .debug_routes import debug_routes

__all__ = [
    'pacientes_routes',
    'acompanhamentos_routes',
    'auth_bp',
    'user_routes',
    'convenio_plano_routes',
    'cep_routes',
    'debug_routes'
    'auth_bp'
]