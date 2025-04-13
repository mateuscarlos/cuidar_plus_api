import pytest
import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos apenas o que existe na aplicação
from app import app
from db import db
from models.user import User
from models.pacientes import Paciente
from models.acompanhamento import Acompanhamento
from models.convenio import Convenio
from models.plano import Plano
from models.setores_funcoes import Setor, Funcao  # Importar tabelas referenciadas

@pytest.fixture(scope='module')
def test_client():
    """Cria um cliente de teste para a aplicação Flask"""
    # Configuração específica para testes
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Cria tabelas no banco de dados de teste
    with app.app_context():
        db.create_all()
        
        # Criar registros necessários para setores e funções
        try:
            # Criar setores e funções base para testes
            setor_ti = Setor(nome="TI")
            setor_adm = Setor(nome="Administração")
            setor_vendas = Setor(nome="Vendas")
            setor_rh = Setor(nome="RH")
            setor_dir = Setor(nome="Diretoria")
            
            funcao_dev = Funcao(nome="Desenvolvedor")
            funcao_gerente = Funcao(nome="Gerente")
            funcao_analista = Funcao(nome="Analista")
            funcao_vendedor = Funcao(nome="Vendedor")
            
            db.session.add_all([
                setor_ti, setor_adm, setor_vendas, setor_rh, setor_dir,
                funcao_dev, funcao_gerente, funcao_analista, funcao_vendedor
            ])
            db.session.commit()
        except Exception as e:
            print(f"Erro ao criar dados base: {e}")
            db.session.rollback()
    
    # Cria um cliente de teste
    with app.test_client() as client:
        with app.app_context():
            yield client
    
    # Limpeza após os testes
    with app.app_context():
        try:
            # Em SQLAlchemy 2.0+, use conexão direta em vez de engine.execute
            with db.engine.connect() as connection:
                # Para SQLite apenas
                connection.execute(db.text("PRAGMA foreign_keys = OFF"))
            
            # Limpar tabelas na ordem correta
            db.session.query(Acompanhamento).delete()
            db.session.query(Paciente).delete()
            db.session.query(Plano).delete()
            db.session.query(Convenio).delete()
            db.session.query(User).delete()
            db.session.commit()
            
            # Dropar todas as tabelas
            db.drop_all()
            
            with db.engine.connect() as connection:
                connection.execute(db.text("PRAGMA foreign_keys = ON"))
                
        except Exception as e:
            print(f"Erro ao limpar banco de dados: {e}")

@pytest.fixture(autouse=True)
def clear_db():
    """Limpa o banco de dados entre os testes"""
    with app.app_context():
        try:
            # Limpar apenas os dados de teste, não as tabelas de referência
            db.session.query(Acompanhamento).delete()
            db.session.query(Paciente).delete()
            db.session.query(Plano).delete()
            db.session.query(Convenio).delete()
            db.session.query(User).delete()
            db.session.commit()
        except Exception as e:
            print(f"Erro ao limpar tabelas entre testes: {e}")
            db.session.rollback()

@pytest.fixture
def create_test_user():
    """Factory fixture para criar usuários de teste"""
    def _create_user(nome='João da Silva', cpf='12345678909', 
                     setor='TI', funcao='Desenvolvedor', 
                     email='joao@example.com', password='senha123',
                     cep='01001000'):  # Adicionando CEP como padrão
        with app.app_context():
            # Encontrar IDs de setor e função
            setor_obj = Setor.query.filter_by(nome=setor).first()
            if not setor_obj:
                setor_obj = Setor(nome=setor)
                db.session.add(setor_obj)
                db.session.commit()
            
            funcao_obj = Funcao.query.filter_by(nome=funcao).first()
            if not funcao_obj:
                funcao_obj = Funcao(nome=funcao)
                db.session.add(funcao_obj)
                db.session.commit()
            
            # Criar usuário completo
            user = User(
                nome=nome, 
                cpf=cpf, 
                setor_id=setor_obj.id,
                funcao_id=funcao_obj.id,
                email=email,
                password_hash=password,  # Ideal seria usar um método set_password se existir
                cep=cep
            )
            
            db.session.add(user)
            db.session.commit()
            # Atualizar a sessão para evitar objetos desanexados
            db.session.refresh(user)
            return user
    return _create_user

@pytest.fixture
def create_test_paciente():
    """Factory fixture para criar pacientes de teste"""
    def _create_paciente(nome_completo='Maria Silva', cpf='98765432100', 
                        data_nascimento='1980-05-15', acomodacao='Apartamento',
                        telefone='(11) 99999-8888', cid_primario='G40'):
        with app.app_context():
            paciente = Paciente(
                nome_completo=nome_completo,
                cpf=cpf,
                data_nascimento=data_nascimento,
                acomodacao=acomodacao,
                telefone=telefone,
                cid_primario=cid_primario
            )
            db.session.add(paciente)
            db.session.commit()
            # Atualizar a sessão para evitar objetos desanexados
            db.session.refresh(paciente)
            return paciente
    return _create_paciente

@pytest.fixture
def create_test_convenio():
    """Factory fixture para criar convênios de teste"""
    def _create_convenio(nome='Convênio Teste'):
        with app.app_context():
            # Verificar os campos válidos para o modelo Convenio
            convenio = Convenio(
                nome=nome
                # Não usar campos que não existem no modelo
            )
            db.session.add(convenio)
            db.session.commit()
            # Atualizar a sessão para evitar objetos desanexados
            db.session.refresh(convenio)
            return convenio
    return _create_convenio

@pytest.fixture
def create_test_acompanhamento():
    """Factory fixture para criar acompanhamentos de teste"""
    def _create_acompanhamento(paciente=None, tipo_atendimento='Consulta', 
                             motivo_atendimento='Avaliação', descricao='Paciente estável'):
        with app.app_context():
            # Se não foi fornecido paciente, criar um
            if paciente is None:
                paciente = Paciente(
                    nome_completo='Paciente Acompanhamento',
                    cpf='11122233344',
                    data_nascimento=date(1990, 1, 1),
                    acomodacao='Enfermaria',
                    telefone='(11) 5555-6666',
                    cid_primario='J45'
                )
                db.session.add(paciente)
                db.session.commit()
                db.session.refresh(paciente)
            
            # Criar acompanhamento com data_hora explícita
            acompanhamento = Acompanhamento(
                paciente_id=paciente.id,
                data_hora=datetime.now(),  # Garantir que data_hora não seja nula
                tipo_atendimento=tipo_atendimento,
                motivo_atendimento=motivo_atendimento,
                descricao=descricao
            )
            db.session.add(acompanhamento)
            db.session.commit()
            db.session.refresh(acompanhamento)
            return acompanhamento
    return _create_acompanhamento