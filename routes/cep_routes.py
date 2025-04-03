from flask import Blueprint, jsonify, request
import requests

cep_routes = Blueprint('cep_routes', __name__)

@cep_routes.route('/cep/<string:cep>', methods=['GET'])
def consultar_cep(cep):
    """Proxy para consultar o CEP na API ViaCEP"""
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        response.raise_for_status()  # Levanta uma exceção para códigos de erro HTTP
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500