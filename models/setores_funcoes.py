from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app import db  # Retain this import and remove the redundant one

class Setor(db.Model):
    __tablename__ = 'setores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    funcoes = db.relationship("Funcao", backref="setor", lazy=True)

    def __repr__(self):
        return f"<Setor {self.nome}>"


class Funcao(db.Model):
    __tablename__ = 'funcoes'

    id = db.Column(db.Integer, primary_key=True)
    setor_id = db.Column(db.Integer, db.ForeignKey('setores.id'), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    conselho_profissional = db.Column(db.String(50), nullable=True)
    especializacao_recomendada = db.Column(db.String(255), nullable=True)
    tipo_contratacao = db.Column(db.Enum('c', 't', 'p'), nullable=False)  # c = contratado, t = terceirizado, p = pessoa jurídica

    def __repr__(self):
        return f"<Funcao {self.nome}>"

    @property
    def tipo_contratacao_extenso(self):
        tipos = {
            'c': 'Contratação Direta',
            't': 'Terceirizável',
            'p': 'Pessoa Jurídica'
        }
        return tipos.get(self.tipo_contratacao, 'Desconhecido')
