from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy instance
db = SQLAlchemy()

# Define models
class Setor(db.Model):
    __tablename__ = 'setores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Setor {self.nome}>'

class Funcao(db.Model):
    __tablename__ = 'funcoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    setor_id = db.Column(db.Integer, db.ForeignKey('setores.id'), nullable=False)
    conselho_profissional = db.Column(db.String(100), nullable=True)
    especializacao_recomendada = db.Column(db.String(200), nullable=True)
    tipo_contratacao = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Funcao {self.nome}>'