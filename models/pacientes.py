from db import db

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    operadora = db.Column(db.String(50), nullable=False)
    cid_primario = db.Column(db.String(10), nullable=False)
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(50))
    cep = db.Column(db.String(8), nullable=False)
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))

    def __repr__(self):
        return f'<Paciente {self.nome_completo}>'