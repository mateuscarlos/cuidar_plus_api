from flask import Blueprint, jsonify, request
import requests

cep_routes = Blueprint('cep_routes', __name__)

@cep_routes.route('/cep/<string:cep>', methods=['GET'])
def consultar_cep(cep):
    """
    Proxy para consultar o CEP na API ViaCEP
    
    Retorna os dados do CEP exatamente como fornecidos pela API ViaCEP,
    preservando todos os campos originais (cep, logradouro, complemento, 
    bairro, localidade, uf, ibge, gia, ddd, siafi).
    """
    try:
        # Formatar o CEP removendo caracteres não numéricos
        cep_limpo = ''.join(filter(str.isdigit, cep))
        
        # Verificar se o CEP tem 8 dígitos
        if len(cep_limpo) != 8:
            return jsonify({'error': 'CEP inválido. Deve conter 8 dígitos.'}), 400
            
        # Fazer a requisição para a API ViaCEP
        response = requests.get(f'https://viacep.com.br/ws/{cep_limpo}/json/')
        response.raise_for_status()  # Levanta uma exceção para códigos de erro HTTP
        
        # Verificar se a API retornou um erro
        data = response.json()
        if 'erro' in data and data['erro']:
            return jsonify({'error': 'CEP não encontrado'}), 404
            
        # Retornar o JSON exatamente como recebido da API ViaCEP
        return jsonify(data), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro ao consultar o serviço de CEP: {str(e)}'}), 500