from db import db
from datetime import datetime

class Acompanhamento(db.Model):
    __tablename__ = 'acompanhamentos'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    paciente = db.relationship('Paciente', backref=db.backref('acompanhamentos', lazy=True))
    usuario = db.relationship('User', backref=db.backref('acompanhamentos', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
            'paciente_id': self.paciente_id,
            'usuario_id': self.usuario_id
        }