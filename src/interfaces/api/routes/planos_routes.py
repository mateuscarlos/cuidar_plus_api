from flask import Blueprint, jsonify
from models.plano import Plano

planos_routes = Blueprint('planos_routes', __name__)

@planos_routes.route('/planos', methods=['GET'])
def listar_planos():
    """Listar todos os planos"""
    try:
        planos = Plano.query.all()
        resultado = [plano.to_dict() for plano in planos]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500