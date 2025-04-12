from flask import Blueprint, jsonify, request
import requests
from flasgger import swag_from

cep_routes = Blueprint('cep_routes', __name__)

@cep_routes.route('/cep/<string:cep>', methods=['GET'])
def consultar_cep(cep):
    """
    Consultar endereço pelo CEP
    ---
    tags:
      - Endereços
    parameters:
      - name: cep
        in: path
        type: string
        required: true
        description: CEP a ser consultado (somente números ou no formato 00000-000)
        example: "01001000"
    responses:
      200:
        description: Dados do endereço correspondente ao CEP
        schema:
          type: object
          properties:
            cep:
              type: string
              example: "01001-000"
            logradouro:
              type: string
              example: "Praça da Sé"
            complemento:
              type: string
              example: "lado ímpar"
            bairro:
              type: string
              example: "Sé"
            localidade:
              type: string
              example: "São Paulo"
            uf:
              type: string
              example: "SP"
            ibge:
              type: string
              example: "3550308"
            gia:
              type: string
              example: "1004"
            ddd:
              type: string
              example: "11"
            siafi:
              type: string
              example: "7107"
      400:
        description: CEP inválido
        schema:
          type: object
          properties:
            error:
              type: string
              example: "CEP inválido. Deve conter 8 dígitos."
      404:
        description: CEP não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "CEP não encontrado"
      500:
        description: Erro no serviço
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao consultar o serviço de CEP: Connection error"
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

@cep_routes.route('/endereco', methods=['GET'])
def consultar_endereco_por_logradouro():
    """
    Pesquisar endereço por logradouro/cidade/estado
    ---
    tags:
      - Endereços
    parameters:
      - name: uf
        in: query
        type: string
        required: true
        description: Sigla do estado com 2 caracteres
        example: "SP"
      - name: cidade
        in: query
        type: string
        required: true
        description: Nome da cidade
        example: "São Paulo"
      - name: logradouro
        in: query
        type: string
        required: true
        description: Nome do logradouro (min. 3 caracteres)
        example: "Avenida Paulista"
    responses:
      200:
        description: Lista de endereços correspondentes à pesquisa
        schema:
          type: array
          items:
            type: object
            properties:
              cep:
                type: string
                example: "01310-100"
              logradouro:
                type: string
                example: "Avenida Paulista"
              complemento:
                type: string
                example: "de 1 a 610 - lado par"
              bairro:
                type: string
                example: "Bela Vista"
              localidade:
                type: string
                example: "São Paulo"
              uf:
                type: string
                example: "SP"
              ibge:
                type: string
                example: "3550308"
              gia:
                type: string
                example: "1004"
              ddd:
                type: string
                example: "11"
              siafi:
                type: string
                example: "7107"
      400:
        description: Parâmetros inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Os parâmetros uf, cidade e logradouro são obrigatórios. O logradouro deve ter pelo menos 3 caracteres."
      404:
        description: Endereço não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Nenhum endereço encontrado com os parâmetros fornecidos"
      500:
        description: Erro no serviço
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao consultar o serviço de CEP: Connection error"
    """
    try:
        # Obter parâmetros da consulta
        uf = request.args.get('uf')
        cidade = request.args.get('cidade')
        logradouro = request.args.get('logradouro')
        
        # Validar parâmetros
        if not uf or not cidade or not logradouro or len(logradouro) < 3:
            return jsonify({'error': 'Os parâmetros uf, cidade e logradouro são obrigatórios. O logradouro deve ter pelo menos 3 caracteres.'}), 400
        
        # Fazer requisição para a API ViaCEP usando o endpoint de pesquisa por endereço
        response = requests.get(f'https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/')
        response.raise_for_status()
        
        # Verificar se a resposta é válida
        data = response.json()
        if not data or (isinstance(data, dict) and 'erro' in data):
            return jsonify({'error': 'Nenhum endereço encontrado com os parâmetros fornecidos'}), 404
        
        # Retornar a lista de endereços encontrados
        return jsonify(data), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro ao consultar o serviço de CEP: {str(e)}'}), 500