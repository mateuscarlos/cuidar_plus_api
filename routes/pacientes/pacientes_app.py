from flask import Blueprint
from .create_paciente import create_paciente
from .update_paciente import atualizar_paciente
from .delete_paciente import excluir_paciente
from .get_paciente import buscar_paciente
from .get_all_pacientes import get_all_pacientes
from .get_paciente_by_id import get_paciente_by_id

pacientes_routes = Blueprint('pacientes_routes', __name__)

pacientes_routes.route('/api/criar_paciente', methods=['POST'])(create_paciente)
pacientes_routes.route('/api/atualizar_paciente/<int:paciente_id>', methods=['PUT'])(atualizar_paciente)
pacientes_routes.route('/api/excluir_paciente/<int:paciente_id>', methods=['DELETE'])(excluir_paciente)
pacientes_routes.route('/api/buscar_paciente', methods=['GET'])(buscar_paciente)
pacientes_routes.route('/api/exibe_pacientes', methods=['GET'])(get_all_pacientes)
pacientes_routes.route('/api/paciente/<int:id>', methods=['GET'])(get_paciente_by_id)