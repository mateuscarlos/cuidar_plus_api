from datetime import datetime
from db import db

class Paciente(db.Model):
    __tablename__ = 'paciente'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    operadora = db.Column(db.String(50), nullable=False)
    identificador_prestadora = db.Column(db.String(50), nullable=False)
    acomodacao = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    alergias = db.Column(db.Text, nullable=True)
    cid_primario = db.Column(db.String(10), nullable=False)
    cid_secundario = db.Column(db.String(10), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=False)
    rua = db.Column(db.String(100), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(50), nullable=True)
    cep = db.Column(db.String(8), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='em-avaliacao')  # Adiciona o campo de status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'cpf': self.cpf,
            'updated_at': self.updated_at
        }