from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    rua = db.Column(db.String(100), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(50), nullable=True)
    cep = db.Column(db.String(8), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    setor = db.Column(db.String(50))
    funcao = db.Column(db.String(50))
    especialidade = db.Column(db.String(50))
    registro_categoria = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    data_admissao = db.Column(db.Date)
    status = db.Column(db.String(20))
    tipo_acesso = db.Column(db.String(20))

    def __repr__(self):
        return f'<User  {self.nome}>'