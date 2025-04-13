from db import db
import json
from sqlalchemy import Column, Integer, String, Text

class Endereco:
    """
    Classe modelo para representar um endereço.
    Esta classe não é uma tabela do banco de dados, mas um tipo de dado JSON.
    Usa as mesmas nomenclaturas da API ViaCEP para facilitar a interoperabilidade.
    """
    def __init__(self, cep=None, logradouro=None, complemento=None, bairro=None, 
                 localidade=None, uf=None, ibge=None, gia=None, ddd=None, siafi=None,
                 numero=None, unidade=None, estado=None, regiao=None):
        # Campos padrão da API ViaCEP
        self.cep = cep
        self.logradouro = logradouro
        self.complemento = complemento
        self.bairro = bairro
        self.localidade = localidade  # Cidade
        self.uf = uf                  # Estado (sigla)
        self.ibge = ibge
        self.gia = gia
        self.ddd = ddd
        self.siafi = siafi
        self.unidade = unidade
        self.estado = estado          # Nome do estado por extenso
        self.regiao = regiao          # Nome da região
        
        # Campo adicional não presente na API ViaCEP mas necessário
        self.numero = numero
    
    def to_dict(self):
        """Converte o objeto Endereco para um dicionário"""
        return {
            'cep': self.cep,
            'logradouro': self.logradouro,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'localidade': self.localidade,
            'uf': self.uf,
            'ibge': self.ibge,
            'gia': self.gia,
            'ddd': self.ddd,
            'siafi': self.siafi,
            'unidade': self.unidade,
            'estado': self.estado,
            'regiao': self.regiao,
            'numero': self.numero
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria um objeto Endereco a partir de um dicionário"""
        return cls(
            cep=data.get('cep'),
            logradouro=data.get('logradouro'),
            complemento=data.get('complemento'),
            bairro=data.get('bairro'),
            localidade=data.get('localidade'),
            uf=data.get('uf'),
            ibge=data.get('ibge'),
            gia=data.get('gia'),
            ddd=data.get('ddd'),
            siafi=data.get('siafi'),
            unidade=data.get('unidade'),
            estado=data.get('estado'),
            regiao=data.get('regiao'),
            numero=data.get('numero')
        )
    
    def to_json(self):
        """Converte o objeto para uma string JSON"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str):
        """Cria um objeto Endereco a partir de uma string JSON"""
        if not json_str:
            return None
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except json.JSONDecodeError:
            return None