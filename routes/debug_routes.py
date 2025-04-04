from flask import Blueprint, jsonify
from models.plano import Plano
from models.convenio import Convenio

debug_routes = Blueprint('debug_routes', __name__)

@debug_routes.route('/debug/relacionamentos', methods=['GET'])
def mostrar_relacionamentos():
    """Mostrar relacionamentos entre convênios e planos para debugging"""
    try:
        convenios = Convenio.query.all()
        resultado = []
        
        for convenio in convenios:
            planos = Plano.query.filter_by(convenio_id=convenio.id).all()
            
            convenio_data = {
                'id': convenio.id,
                'nome': convenio.nome,
                'planos': [
                    {
                        'id': plano.id,
                        'nome': plano.nome,
                        'convenio_id': plano.convenio_id
                    }
                    for plano in planos
                ]
            }
            resultado.append(convenio_data)
            
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500