from argon2 import PasswordHasher
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from db import db
from models.user import User

def create_root_user():
    """
    Cria um usuário root com privilégios administrativos completos.
    """
    ph = PasswordHasher()
    
    with app.app_context():
        # Verifica se o usuário root já existe
        existing_user = User.query.filter_by(email='admin@cuidarplus.com').first()
        
        if existing_user:
            print("Usuário root já existe!")
            return
        
        # Cria o usuário root
        root_user = User(
            nome="Administrador",
            email="admin@cuidarplus.com",
            password_hash=ph.hash("CuidarPlus@2025"),  # Senha forte para demonstração
            cargo="Administrador",
            permissions=["admin", "view_all", "edit_all", "delete_all"]  # Todas as permissões
        )
        
        try:
            db.session.add(root_user)
            db.session.commit()
            print("Usuário root criado com sucesso!")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar usuário root: {e}")

if __name__ == "__main__":
    create_root_user()