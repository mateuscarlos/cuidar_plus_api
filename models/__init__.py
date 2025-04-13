# Make models a proper Python package
from db import db  # Import db to make it available to all models

# Import all models to make them accessible from models package
from .pacientes import Paciente
from .acompanhamento import Acompanhamento
from .convenio import Convenio
from .plano import Plano
from .user import User
from .setores_funcoes import Setor, Funcao
# Import other models as needed