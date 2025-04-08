from db import db  # Keep only this import
from flask import jsonify

class Setor(db.Model):
    __tablename__ = 'setores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    funcoes = db.relationship("Funcao", backref="setor", lazy=True)

    def __repr__(self):
        return f"<Setor {self.nome}>"

    @staticmethod
    def get_setores_dict():
        setores = Setor.query.all()
        return {setor.id: setor.nome for setor in setores}


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

    @staticmethod
    def get_funcoes_dict():
        funcoes = Funcao.query.all()
        return {funcao.id: funcao.nome for funcao in funcoes}

    @property
    def tipo_contratacao_extenso(self):
        tipos = {
            'c': 'Contratação Direta',
            't': 'Terceirizável',
            'p': 'Pessoa Jurídica'
        }
        return tipos.get(self.tipo_contratacao, 'Desconhecido')
