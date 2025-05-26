# Make models a proper Python package
from db import db  # Import db to make it available to all models

# Import all models to make them accessible from models package
from models.setor import Setor
from models.funcao import Funcao
from models.user import User
from models.pacientes import Paciente
from models.endereco import Endereco
from models.convenio import Convenio
from models.plano import Plano
from models.acompanhamento import Acompanhamento
from models.views import FuncaoSetorView

__all__ = [
    'Setor',
    'Funcao', 
    'User',
    'Paciente',
    'Endereco',
    'Convenio',
    'Plano',
    'Acompanhamento',
    'FuncaoSetorView'
]