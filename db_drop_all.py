from src.interfaces.api.app import app
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
        connection.execute(text("DROP TABLE IF EXISTS users"))
        connection.execute(text("DROP TABLE IF EXISTS convenio"))
        connection.execute(text("DROP TABLE IF EXISTS user"))
        connection.execute(text("DROP TABLE IF EXISTS plano"))
        connection.execute(text("DROP TABLE IF EXISTS tratamento"))

        
        # Habilitar verificações de chaves estrangeiras novamente
        connection.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    
    print("Todas as tabelas foram removidas.")