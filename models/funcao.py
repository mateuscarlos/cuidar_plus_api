from db import db
from datetime import datetime

class Funcao(db.Model):
    __tablename__ = 'funcoes'

    id = db.Column(db.Integer, primary_key=True)
    setor_id = db.Column(db.Integer, db.ForeignKey('setores.id'), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    nivel_acesso = db.Column(db.Integer, nullable=False, default=1)  # 1=Básico, 2=Intermediário, 3=Avançado
    status = db.Column(db.Boolean, default=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    reg_categoria = db.Column(db.String(100), nullable=True)  # Categoria do registro profissional

    def __repr__(self):
        return f"<Funcao {self.nome} - Setor: {self.setor.nome if self.setor else 'N/A'}>"

    def to_dict(self):
        return {
            'id': self.id,
            'setor_id': self.setor_id,
            'nome': self.nome,
            'descricao': self.descricao,
            'nivel_acesso': self.nivel_acesso,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'reg_categoria': self.reg_categoria,
            'setor_nome': self.setor.nome if self.setor else None
        }

    @staticmethod
    def get_funcoes_dict():
        funcoes = Funcao.query.filter_by(status=True).all()
        return {funcao.id: funcao.nome for funcao in funcoes}

    @staticmethod
    def get_funcoes_por_setor(setor_id):
        return Funcao.query.filter_by(setor_id=setor_id, status=True).all()

    @staticmethod
    def get_funcoes_ativas():
        return Funcao.query.filter_by(status=True).all()