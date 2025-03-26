from datetime import datetime
from db import db

class Plano(db.Model):
    __tablename__ = 'plano'
    
    id = db.Column(db.Integer, primary_key=True)
    convenio_id = db.Column(db.Integer, db.ForeignKey('convenio.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), nullable=True)
    tipo_acomodacao = db.Column(db.String(50), nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'convenio_id': self.convenio_id,
            'nome': self.nome,
            'codigo': self.codigo,
            'tipo_acomodacao': self.tipo_acomodacao,
            'ativo': self.ativo,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }