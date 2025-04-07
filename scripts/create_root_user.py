import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.interfaces.api.app import app
from src.infrastructure.database.models.user import User
from src.infrastructure.database.db_config import db
from src.infrastructure.security.password_service import PasswordService
from datetime import datetime

def create_root_user():
    """Cria um usuário administrador root para uso em testes e desenvolvimento"""
    with app.app_context():
        # Verificar se já existe um usuário admin
        existing_admin = User.query.filter_by(email='admin@cuidarmais.com').first()
        if existing_admin:
            print("Usuário root já existe!")
            return
            
        password_service = PasswordService()
        password_hash = password_service.hash_password('admin123')
        
        # Criar o usuário admin
        admin_user = User(
            nome='Administrador',
            cpf='00000000000',
            email='admin@cuidarmais.com',
            setor='Administração',
            funcao='Administrador',
            status='Ativo',
            tipo_acesso='admin',
            password_hash=password_hash,
            data_admissao=datetime.now().date()
        )
        
        db.session.add(admin_user)
        db.session.commit()
        print("Usuário root criado com sucesso!")

if __name__ == '__main__':
    create_root_user()