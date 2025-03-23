from datetime import datetime
from db import db

class Tratamento(db.Model):
    __tablename__ = 'tratamento'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    medicamento = db.Column(db.String(100), nullable=False)
    posologia = db.Column(db.String(200), nullable=False)
    frequencia = db.Column(db.String(50), nullable=False)
    duracao = db.Column(db.String(50), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='ativo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'medicamento': self.medicamento,
            'posologia': self.posologia,
            'frequencia': self.frequencia,
            'duracao': self.duracao,
            'data_inicio': self.data_inicio.strftime('%Y-%m-%d') if self.data_inicio else None,
            'data_fim': self.data_fim.strftime('%Y-%m-%d') if self.data_fim else None,
            'observacoes': self.observacoes,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }