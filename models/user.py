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
    cep = db.Column(db.String(10), nullable=False)
    _endereco = db.Column(db.Text)
    
    # Foreign keys para os novos modelos
    setor_id = db.Column(db.Integer, db.ForeignKey('setores.id'), nullable=True)
    funcao_id = db.Column(db.Integer, db.ForeignKey('funcoes.id'), nullable=True)
    
   
    especialidade = db.Column(db.String(50))
    registro_categoria = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    data_admissao = db.Column(db.Date)
    status = db.Column(db.String(20), default='Ativo')
    tipo_acesso = db.Column(db.String(20))
    _permissions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tipo_contratacao = db.Column(db.String(30), nullable=True)
    conselho_profissional = db.Column(db.String(50), nullable=True)

    # Campos legacy para compatibilidade
    setor = db.Column(db.String(50))  # Campo legacy
    funcao = db.Column(db.String(50))  # Campo legacy

    # Relacionamentos
    setor_rel = db.relationship("Setor", foreign_keys=[setor_id], backref="usuarios")
    funcao_rel = db.relationship("Funcao", foreign_keys=[funcao_id], backref="usuarios")

    @property
    def endereco(self):
        if self._endereco:
            return json.loads(self._endereco)
        return {}

    @endereco.setter
    def endereco(self, value):
        if value:
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
            'cep': self.cep,
            'endereco': self.endereco,
            'setor_id': self.setor_id,
            'funcao_id': self.funcao_id,
            'setor': self.setor or (self.setor_rel.nome if self.setor_rel else None),  # Compatibilidade
            'funcao': self.funcao or (self.funcao_rel.nome if self.funcao_rel else None),  # Compatibilidade
            'setor_rel': self.setor_rel.to_dict() if self.setor_rel else None,
            'funcao_rel': self.funcao_rel.to_dict() if self.funcao_rel else None,
            'especialidade': self.especialidade,
            'registro_categoria': self.registro_categoria,
            'telefone': self.telefone,
            'data_admissao': self.data_admissao.isoformat() if self.data_admissao else None,
            'status': self.status,
            'tipo_acesso': self.tipo_acesso,
            'permissions': self.permissions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tipo_contratacao': self.tipo_contratacao,
            'conselho_profissional': self.conselho_profissional
        }

    def __repr__(self):
        return f'<User {self.nome}>'