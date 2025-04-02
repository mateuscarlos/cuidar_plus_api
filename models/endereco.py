from db import db
import json
from sqlalchemy import Column, Integer, String, Text

class Endereco:
    """
    Classe modelo para representar um endereço.
    Esta classe não é uma tabela do banco de dados, mas um tipo de dado JSON.
    """
    def __init__(self, rua=None, numero=None, complemento=None, cep=None, bairro=None, cidade=None, estado=None):
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.cep = cep
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
    
    def to_dict(self):
        """Converte o objeto Endereco para um dicionário"""
        return {
            'rua': self.rua,
            'numero': self.numero,
            'complemento': self.complemento,
            'cep': self.cep,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria um objeto Endereco a partir de um dicionário"""
        if data is None:
            return None
        return cls(
            rua=data.get('rua'),
            numero=data.get('numero'),
            complemento=data.get('complemento'),
            cep=data.get('cep'),
            bairro=data.get('bairro'),
            cidade=data.get('cidade'),
            estado=data.get('estado')
        )
    
    def to_json(self):
        """Converte o objeto para uma string JSON"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str):
        """Cria um objeto Endereco a partir de uma string JSON"""
        if not json_str:
            return None
        data = json.loads(json_str)
        return cls.from_dict(data)