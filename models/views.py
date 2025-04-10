from db import db

class FuncaoSetorView(db.Model):
    __tablename__ = 'VW_funcoes_setores'
    
    # Defina aqui as colunas que estão na sua view
    # Por exemplo:
    id_funcao = db.Column(db.Integer, primary_key=True)
    nome_funcao = db.Column(db.String(100))
    id_setor = db.Column(db.Integer)
    nome_setor = db.Column(db.String(100))
    especializacao_recomendada = db.Column(db.String(150))
    
    # Como é uma view, definimos para não tentar atualizar a tabela durante as migrações
    __table_args__ = {'extend_existing': True}