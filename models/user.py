from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
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
    telefone = db.Column(db.String(15))
    data_admissao = db.Column(db.Date)
    status = db.Column(db.String(20))
    tipo_acesso = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User  {self.nome}>'