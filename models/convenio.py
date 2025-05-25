from datetime import datetime
from db import db

class Convenio(db.Model):
    __tablename__ = 'convenio'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), nullable=True)
    tipo = db.Column(db.String(50), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    planos = db.relationship('Plano', backref='convenio', lazy=True, cascade="all, delete-orphan")
    pacientes = db.relationship('Paciente', backref='convenio', lazy=True)
    
    def to_dict(self, include_planos=False):
        data = {
            'id': self.id,
            'nome': self.nome,
            'codigo': self.codigo,
            'tipo': self.tipo,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'observacoes': self.observacoes,
            'ativo': self.ativo,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
        
        if include_planos:
            data['planos'] = [plano.to_dict() for plano in self.planos] if self.planos else []
            
        return data