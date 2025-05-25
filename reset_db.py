from sqlalchemy import inspect, text
from db import db
from flask import Flask
import os

# Configurar app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    print("🗑️  Removendo todas as tabelas...")
    
    # Dropar todas as tabelas
    db.drop_all()
    
    print("✅ Todas as tabelas removidas!")
    
    # Recriar todas as tabelas com base nos modelos atuais
    print("🔨 Criando tabelas com base nos modelos...")
    db.create_all()
    
    print("✅ Tabelas criadas com sucesso!")
    
    # Verificar tabelas criadas
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print("📋 Tabelas criadas:")
    for table in tables:
        columns = [col['name'] for col in inspector.get_columns(table)]
        print(f"  - {table}: {columns}")
