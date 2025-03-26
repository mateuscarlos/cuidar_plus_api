from flask import Blueprint
from .get_paciente import buscar_paciente
from .exibe_paciente import exibir_paciente, exibir_pacientes
from routes.pacientes.create_paciente import create_paciente
from .update_paciente import atualizar_paciente
from .delete_paciente import excluir_paciente

pacientes_routes = Blueprint('pacientes', __name__, url_prefix='/api')

# Rotas de pacientes
pacientes_routes.route('/exibe_pacientes', methods=['GET'])(exibir_pacientes)
pacientes_routes.route('/exibe_paciente/<int:id>', methods=['GET'])(exibir_paciente)
pacientes_routes.route('/criar_paciente', methods=['GET'])(create_paciente)
#pacientes_routes.route('/cadastra_paciente', methods=['POST'])(cadastrar_paciente)
pacientes_routes.route('/atualiza_paciente/<int:id>', methods=['PUT'])(atualizar_paciente)
pacientes_routes.route('/excluir_paciente/<int:id>', methods=['DELETE'])(excluir_paciente)