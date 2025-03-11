from app import app
from db import db
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as connection:
        # Desabilitar verificações de chaves estrangeiras
        connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        
        # Drop tabelas na ordem correta
        connection.execute(text("DROP TABLE IF EXISTS acompanhamentos"))
        connection.execute(text("DROP TABLE IF EXISTS usuario"))
        connection.execute(text("DROP TABLE IF EXISTS paciente"))
        
        # Habilitar verificações de chaves estrangeiras novamente
        connection.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    
    print("Tabelas acompanhamentos, usuario e paciente foram removidas.")