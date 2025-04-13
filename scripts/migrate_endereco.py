from models.pacientes import Paciente
from models.endereco import Endereco
from db import db
import sys
sys.path.append('..')

def migrate_endereco():
    """Migra os dados de endereço para o formato JSON"""
    pacientes = Paciente.query.all()
    
    for paciente in pacientes:
        # Criar o objeto de endereço
        endereco = Endereco(
            rua=paciente.rua,
            numero=paciente.numero,
            complemento=paciente.complemento,
            cep=paciente.cep,
            bairro=paciente.bairro,
            cidade=paciente.cidade,
            estado=paciente.estado
        )
        
        # Definir o JSON de endereço
        paciente.endereco = endereco
    
    # Salvar as alterações
    db.session.commit()
    print("Migração de endereços concluída com sucesso.")

if __name__ == "__main__":
    # Importar o app para pegar o contexto da aplicação
    from app import app
    with app.app_context():
        migrate_endereco()