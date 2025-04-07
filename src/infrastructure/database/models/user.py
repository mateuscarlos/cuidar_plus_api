from datetime import datetime
from src.infrastructure.database.db_config import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(50))
    cep = db.Column(db.String(8))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))
    setor = db.Column(db.String(50), nullable=False)
    funcao = db.Column(db.String(50), nullable=False)
    especialidade = db.Column(db.String(50))
    registro_categoria = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    data_admissao = db.Column(db.Date)
    status = db.Column(db.String(20), default='Ativo')
    tipo_acesso = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.nome}>'
    
    def to_dict(self):
        """Converte o objeto em um dicionário para serialização"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf,
            'setor': self.setor,
            'funcao': self.funcao,
            'status': self.status,
            'tipo_acesso': self.tipo_acesso
        }