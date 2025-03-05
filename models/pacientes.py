from datetime import datetime
from db import db

class Paciente(db.Model):
    __tablename__ = 'paciente'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    operadora = db.Column(db.String(50), nullable=False)
    cid_primario = db.Column(db.String(10), nullable=False)
    rua = db.Column(db.String(100), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(50), nullable=True)
    cep = db.Column(db.String(8), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)