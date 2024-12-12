from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    endereco = db.Column(db.String(200))
    setor = db.Column(db.String(50))
    funcao = db.Column(db.String(50))
    especialidade = db.Column(db.String(50))
    registro_categoria = db.Column(db.String(50))

    def __repr__(self):
        return f'<User  {self.nome}>'