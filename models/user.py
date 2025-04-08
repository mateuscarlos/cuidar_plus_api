from db import db
import json
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.String(50))
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    cep = db.Column(db.String(10), nullable=False)  # CEP obrigatório
    _endereco = db.Column(db.Text)  # Armazena o restante do endereço como JSON
    setor = db.Column(db.String(50), nullable=False)
    funcao = db.Column(db.String(50), nullable=False)
    especialidade = db.Column(db.String(50))
    registro_categoria = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    data_admissao = db.Column(db.Date)
    status = db.Column(db.String(20), default='Ativo')
    tipo_acesso = db.Column(db.String(20))
    _permissions = db.Column(db.Text)  # Armazena permissões como JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def endereco(self):
        if self._endereco:
            return json.loads(self._endereco)
        return {}

    @endereco.setter
    def endereco(self, value):
        if value:
            # Removemos a validação de CEP pois agora está separado
            self._endereco = json.dumps(value)
        else:
            self._endereco = None

    @property
    def permissions(self):
        if self._permissions:
            return json.loads(self._permissions)
        return []

    @permissions.setter
    def permissions(self, value):
        if value:
            self._permissions = json.dumps(value)
        else:
            self._permissions = None

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cargo': self.cargo,
            'cpf': self.cpf,
            'cep': self.cep,  # Incluímos o CEP aqui
            'setor': self.setor,
            'funcao': self.funcao,
            'endereco': self.endereco,
            'permissions': self.permissions
        }

    def __repr__(self):
        return f'<User {self.nome}>'