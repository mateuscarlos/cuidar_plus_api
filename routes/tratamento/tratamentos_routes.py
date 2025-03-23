from flask import Blueprint
from .get_tratamentos import get_tratamentos
from .create_tratamento import create_tratamento
from .get_tratamentos_by_pacientes import get_tratamentos_by_paciente
from .get_tratamento import get_tratamento
from .update_tratamento import update_tratamento
from .delete_tratamento import delete_tratamento

tratamentos_routes = Blueprint('tratamentos_routes', __name__)

# Rotas
tratamentos_routes.route('/api/tratamentos', methods=['GET'])(get_tratamentos)
tratamentos_routes.route('/api/criar_tratamento', methods=['POST'])(create_tratamento)
tratamentos_routes.route('/api/pacientes/<int:paciente_id>/tratamentos', methods=['GET'])(get_tratamentos_by_paciente)
tratamentos_routes.route('/api/tratamentos/<int:tratamento_id>', methods=['GET'])(get_tratamento)
tratamentos_routes.route('/api/tratamentos/<int:tratamento_id>', methods=['PUT'])(update_tratamento)
tratamentos_routes.route('/api/tratamentos/<int:tratamento_id>', methods=['DELETE'])(delete_tratamento)