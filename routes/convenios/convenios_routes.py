from flask import Blueprint
from .get_convenios import get_convenios
from .get_planos_by_convenio import get_planos_by_convenio
from .create_convenio import create_convenio
from .update_convenio import update_convenio
from .delete_convenio import delete_convenio
from .get_convenio_by_id import get_convenio_by_id
from .create_plano import create_plano
from .update_plano import update_plano
from .delete_plano import delete_plano
from .get_plano_by_id import get_plano_by_id

convenios_routes = Blueprint('convenios_routes', __name__)

# Rotas para Convênios
convenios_routes.route('/convenios', methods=['GET'])(get_convenios)
convenios_routes.route('/convenios/<int:convenio_id>', methods=['GET'])(get_convenio_by_id)
convenios_routes.route('/convenios', methods=['POST'])(create_convenio)
convenios_routes.route('/convenios/<int:convenio_id>', methods=['PUT'])(update_convenio)
convenios_routes.route('/convenios/<int:convenio_id>', methods=['DELETE'])(delete_convenio)

# Rotas para Planos
convenios_routes.route('/convenios/<int:convenio_id>/planos', methods=['GET'])(get_planos_by_convenio)
convenios_routes.route('/convenios/<int:convenio_id>/planos', methods=['POST'])(create_plano)
convenios_routes.route('/convenios/<int:convenio_id>/planos/<int:plano_id>', methods=['GET'])(get_plano_by_id)
convenios_routes.route('/convenios/<int:convenio_id>/planos/<int:plano_id>', methods=['PUT'])(update_plano)
convenios_routes.route('/convenios/<int:convenio_id>/planos/<int:plano_id>', methods=['DELETE'])(delete_plano)