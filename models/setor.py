from db import db
from datetime import datetime
import datetime as dt

class Setor(db.Model):
    __tablename__ = 'setores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    status = db.Column(db.Boolean, default=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.now(dt.timezone.utc), nullable=False)

    # Relacionamento com funções
    funcoes = db.relationship("Funcao", backref="setor", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Setor {self.nome}>"

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'funcoes': [funcao.to_dict() for funcao in (self.funcoes or [])] # type: ignore
        }

    @staticmethod
    def get_setores_dict():
        setores = Setor.query.filter_by(status=True).all()
        return {str(setor.id): setor.nome for setor in setores}

    @staticmethod
    def get_setores_ativos():
        return Setor.query.filter_by(status=True).all()