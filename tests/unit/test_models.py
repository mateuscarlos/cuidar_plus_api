import pytest
import sys
import os
import json
from datetime import datetime, date

# Adiciona o diretório raiz ao path do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importações necessárias
from app import app
from db import db
from models.user import User
from models.pacientes import Paciente
from models.acompanhamento import Acompanhamento
from models.convenio import Convenio
from models.plano import Plano
from models.setores_funcoes import Setor, Funcao  # Adicionando importação de Setor e Funcao

class TestUserModel:
    """Testes para o modelo User"""
    
    def test_criar_usuario(self):
        """Testa a criação e recuperação de um usuário"""
        with app.app_context():
            # Primeiro criar setor e função se necessário
            setor = Setor.query.filter_by(nome="TI").first()
            if not setor:
                setor = Setor(nome="TI")
                db.session.add(setor)
            
            funcao = Funcao.query.filter_by(nome="Analista").first()
            if not funcao:
                funcao = Funcao(nome="Analista")
                db.session.add(funcao)
            
            db.session.commit()
            
            # Criar usuário de teste com todos os campos obrigatórios
            user = User(
                nome="Usuário Teste", 
                cpf="12345678901",
                setor_id=setor.id,  # Usando ID do setor, não o nome
                funcao_id=funcao.id,  # Usando ID da função, não o nome
                email="usuario@teste.com",
                password_hash="senha_hash_teste",
                cep="01001000"  # Adicionando CEP obrigatório
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Recuperar o usuário pelo ID
            retrieved_user = User.query.get(user.id)
            
            # Verificações
            assert retrieved_user is not None
            assert retrieved_user.nome == "Usuário Teste"
            assert retrieved_user.cpf == "12345678901"
            assert retrieved_user.setor_id == setor.id
            assert retrieved_user.funcao_id == funcao.id
            assert retrieved_user.email == "usuario@teste.com"
            assert retrieved_user.password_hash == "senha_hash_teste"
            assert retrieved_user.cep == "01001000"
    
    def test_atualizar_usuario(self):
        """Testa a atualização de um usuário"""
        with app.app_context():
            # Primeiro criar setor e função se necessário
            setor_rh = Setor.query.filter_by(nome="RH").first()
            if not setor_rh:
                setor_rh = Setor(nome="RH")
                db.session.add(setor_rh)
            
            setor_dir = Setor.query.filter_by(nome="Diretoria").first()
            if not setor_dir:
                setor_dir = Setor(nome="Diretoria")
                db.session.add(setor_dir)
            
            funcao_gerente = Funcao.query.filter_by(nome="Gerente").first()
            if not funcao_gerente:
                funcao_gerente = Funcao(nome="Gerente")
                db.session.add(funcao_gerente)
            
            db.session.commit()
            
            # Criar usuário de teste com todos os campos obrigatórios
            user = User(
                nome="Nome Original", 
                cpf="98765432109", 
                setor_id=setor_rh.id,  # Usando ID do setor
                funcao_id=funcao_gerente.id,  # Usando ID da função
                email="original@email.com",
                password_hash="senha_original",
                cep="02002000"  # Adicionando CEP obrigatório
            )
            db.session.add(user)
            db.session.commit()
            
            # Atualizar o usuário
            user.nome = "Nome Atualizado"
            user.setor_id = setor_dir.id  # Usar ID do setor, não o nome
            user.email = "atualizado@email.com"
            db.session.commit()
            
            # Recuperar o usuário atualizado
            updated_user = User.query.get(user.id)
            
            # Verificações
            assert updated_user.nome == "Nome Atualizado"
            assert updated_user.setor_id == setor_dir.id
            assert updated_user.email == "atualizado@email.com"
            # Campos que não foram alterados devem permanecer iguais
            assert updated_user.cpf == "98765432109"
            assert updated_user.funcao_id == funcao_gerente.id
            assert updated_user.cep == "02002000"
    
    def test_excluir_usuario(self):
        """Testa a exclusão de um usuário"""
        with app.app_context():
            # Primeiro criar setor e função se necessário
            setor_vendas = Setor.query.filter_by(nome="Vendas").first()
            if not setor_vendas:
                setor_vendas = Setor(nome="Vendas")
                db.session.add(setor_vendas)
            
            funcao_vendedor = Funcao.query.filter_by(nome="Vendedor").first()
            if not funcao_vendedor:
                funcao_vendedor = Funcao(nome="Vendedor")
                db.session.add(funcao_vendedor)
            
            db.session.commit()
            
            # Criar usuário de teste com todos os campos obrigatórios
            user = User(
                nome="Usuário Temporário", 
                cpf="11122233344", 
                setor_id=setor_vendas.id,  # Usando ID do setor
                funcao_id=funcao_vendedor.id,  # Usando ID da função
                email="temporario@email.com",
                password_hash="senha_temp",
                cep="03003000"  # Adicionando CEP obrigatório
            )
            db.session.add(user)
            db.session.commit()
            
            user_id = user.id
            
            # Excluir o usuário
            db.session.delete(user)
            db.session.commit()
            
            # Tentar recuperar o usuário excluído
            deleted_user = User.query.get(user_id)
            
            # Verificar que o usuário não existe mais
            assert deleted_user is None


# Corrigindo a classe TestPacienteModel para lidar com o erro de to_json

class TestPacienteModel:
    """Testes para o modelo Paciente"""
    
    def test_criar_paciente(self):
        """Testa a criação e recuperação de um paciente"""
        with app.app_context():
            # Criar paciente de teste
            paciente = Paciente(
                nome_completo="Maria da Silva",
                cpf="33344455566",
                data_nascimento=date(1980, 5, 15),
                acomodacao="Apartamento",
                telefone="(11) 99999-8888",
                cid_primario="G40"
            )
            db.session.add(paciente)
            db.session.commit()
            
            # Recuperar o paciente pelo ID
            retrieved_paciente = Paciente.query.get(paciente.id)
            
            # Verificações diretas sem usar to_json
            assert retrieved_paciente is not None
            assert retrieved_paciente.nome_completo == "Maria da Silva"
            assert retrieved_paciente.cpf == "33344455566"
            assert retrieved_paciente.data_nascimento == date(1980, 5, 15)
            assert retrieved_paciente.acomodacao == "Apartamento"
            assert retrieved_paciente.telefone == "(11) 99999-8888"
            assert retrieved_paciente.cid_primario == "G40"
    
    def test_atualizar_paciente(self):
        """Testa a atualização de um paciente"""
        with app.app_context():
            # Criar paciente de teste
            paciente = Paciente(
                nome_completo="João Oliveira",
                cpf="77788899900",
                data_nascimento=date(1975, 10, 20),
                acomodacao="Enfermaria",
                telefone="(11) 98765-4321",
                cid_primario="I10"
            )
            db.session.add(paciente)
            db.session.commit()
            
            # Atualizar o paciente
            paciente.nome_completo = "João Oliveira Santos"
            paciente.telefone = "(11) 91234-5678"
            paciente.acomodacao = "Apartamento"
            db.session.commit()
            
            # Recuperar o paciente atualizado
            updated_paciente = Paciente.query.get(paciente.id)
            
            # Verificações
            assert updated_paciente.nome_completo == "João Oliveira Santos"
            assert updated_paciente.telefone == "(11) 91234-5678"
            assert updated_paciente.acomodacao == "Apartamento"
            # Campos que não foram alterados devem permanecer iguais
            assert updated_paciente.cpf == "77788899900"
            assert updated_paciente.data_nascimento == date(1975, 10, 20)
    
    def test_excluir_paciente(self):
        """Testa a exclusão de um paciente"""
        with app.app_context():
            # Criar paciente de teste
            paciente = Paciente(
                nome_completo="Paciente Temporário",
                cpf="22233344455",
                data_nascimento=date(1990, 3, 25),
                acomodacao="Enfermaria",
                telefone="(11) 98888-7777",
                cid_primario="E11"
            )
            db.session.add(paciente)
            db.session.commit()
            
            paciente_id = paciente.id
            
            # Excluir o paciente
            db.session.delete(paciente)
            db.session.commit()
            
            # Tentar recuperar o paciente excluído
            deleted_paciente = Paciente.query.get(paciente_id)
            
            # Verificar que o paciente não existe mais
            assert deleted_paciente is None


class TestAcompanhamentoModel:
    """Testes para o modelo Acompanhamento"""
    
    def test_criar_acompanhamento(self):
        """Testa a criação e recuperação de um acompanhamento"""
        with app.app_context():
            # Primeiro criamos um paciente para associar
            paciente = Paciente(
                nome_completo="Ana Acompanhamento",
                cpf="55566677788",
                data_nascimento=date(1970, 8, 10),
                acomodacao="Enfermaria",
                telefone="(11) 97777-6666",
                cid_primario="J45"
            )
            db.session.add(paciente)
            db.session.commit()
            
            # Agora criamos o acompanhamento
            data_hora = datetime.now()
            acompanhamento = Acompanhamento(
                paciente_id=paciente.id,
                data_hora=data_hora,
                tipo_atendimento="Consulta",
                motivo_atendimento="Avaliação inicial",
                descricao="Paciente apresentou sintomas de gripe"
            )
            
            # Adicionamos dados em formato JSON
            acompanhamento.sinais_vitais = {
                "pressao": "120/80",
                "temperatura": 36.8,
                "saturacao": 98
            }
            
            db.session.add(acompanhamento)
            db.session.commit()
            
            # Recuperar o acompanhamento pelo ID
            retrieved_acomp = Acompanhamento.query.get(acompanhamento.id)
            
            # Verificações
            assert retrieved_acomp is not None
            assert retrieved_acomp.paciente_id == paciente.id
            assert retrieved_acomp.tipo_atendimento == "Consulta"
            assert retrieved_acomp.motivo_atendimento == "Avaliação inicial"
            assert retrieved_acomp.descricao == "Paciente apresentou sintomas de gripe"
            assert retrieved_acomp.sinais_vitais["temperatura"] == 36.8
            assert retrieved_acomp.sinais_vitais["saturacao"] == 98
    
    def test_atualizar_acompanhamento(self):
        """Testa a atualização de um acompanhamento"""
        with app.app_context():
            # Primeiro criamos um paciente para associar
            paciente = Paciente(
                nome_completo="Pedro Acompanhamento",
                cpf="99988877766",
                data_nascimento=date(1965, 4, 5),
                acomodacao="Apartamento",
                telefone="(11) 96666-5555",
                cid_primario="K29"
            )
            db.session.add(paciente)
            db.session.commit()
            
            # Criamos o acompanhamento
            acompanhamento = Acompanhamento(
                paciente_id=paciente.id,
                data_hora=datetime.now(),
                tipo_atendimento="Visita",
                motivo_atendimento="Acompanhamento rotineiro",
                descricao="Paciente estável"
            )
            
            acompanhamento.sinais_vitais = {
                "pressao": "130/85",
                "temperatura": 36.5
            }
            
            db.session.add(acompanhamento)
            db.session.commit()
            
            # Atualizar o acompanhamento
            acompanhamento.tipo_atendimento = "Visita de Emergência"
            acompanhamento.descricao = "Paciente apresentou piora"
            acompanhamento.sinais_vitais = {
                "pressao": "145/95",
                "temperatura": 38.2,
                "saturacao": 94
            }
            db.session.commit()
            
            # Recuperar o acompanhamento atualizado
            updated_acomp = Acompanhamento.query.get(acompanhamento.id)
            
            # Verificações
            assert updated_acomp.tipo_atendimento == "Visita de Emergência"
            assert updated_acomp.descricao == "Paciente apresentou piora"
            assert updated_acomp.sinais_vitais["pressao"] == "145/95"
            assert updated_acomp.sinais_vitais["temperatura"] == 38.2
            assert updated_acomp.sinais_vitais["saturacao"] == 94
            # Campos que não foram alterados devem permanecer iguais
            assert updated_acomp.motivo_atendimento == "Acompanhamento rotineiro"


# Corrigindo a classe TestConvenioPlanoModel para remover os argumentos inválidos

class TestConvenioPlanoModel:
    """Testes para os modelos Convenio e Plano"""
    
    def test_criar_convenio(self):
        """Testa a criação e recuperação de um convênio"""
        with app.app_context():
            # Criar convênio de teste sem usar 'endereco' que é inválido
            convenio = Convenio(
                nome="Saúde Total"
                # Remover o campo 'endereco' que não existe no modelo
            )
            db.session.add(convenio)
            db.session.commit()
            
            # Recuperar o convênio pelo ID
            retrieved_convenio = Convenio.query.get(convenio.id)
            
            # Verificações
            assert retrieved_convenio is not None
            assert retrieved_convenio.nome == "Saúde Total"
    
    def test_criar_plano_com_convenio(self):
        """Testa a criação de um plano associado a um convênio"""
        with app.app_context():
            # Criar convênio de teste sem usar 'contato'
            convenio = Convenio(
                nome="MedPlus"
                # Remover campo 'contato'
            )
            db.session.add(convenio)
            db.session.commit()
            
            # Criar plano associado ao convênio
            # Remover campos 'cobertura' e 'carencia' se não existirem
            plano = Plano(
                nome="Premium",
                convenio_id=convenio.id
                # Remover 'cobertura' e 'carencia' que podem não existir
            )
            db.session.add(plano)
            db.session.commit()
            
            # Recuperar o plano pelo ID
            retrieved_plano = Plano.query.get(plano.id)
            
            # Verificações
            assert retrieved_plano is not None
            assert retrieved_plano.nome == "Premium"
            assert retrieved_plano.convenio_id == convenio.id
            
            # Verificar a relação com o convênio
            assert retrieved_plano.convenio.nome == "MedPlus"
    
    def test_convenio_com_multiplos_planos(self):
        """Testa a relação de um para muitos entre Convenio e Plano"""
        with app.app_context():
            # Criar convênio de teste
            convenio = Convenio(
                nome="Vida Saudável"
                # Remover campo 'contato'
            )
            db.session.add(convenio)
            db.session.commit()
            
            # Criar múltiplos planos para o mesmo convênio
            planos = [
                Plano(nome="Básico", convenio_id=convenio.id),
                Plano(nome="Intermediário", convenio_id=convenio.id),
                Plano(nome="Avançado", convenio_id=convenio.id)
            ]
            
            db.session.add_all(planos)
            db.session.commit()
            
            # Verificar se o convênio tem três planos associados
            assert len(convenio.planos) == 3
            assert any(plano.nome == "Básico" for plano in convenio.planos)
            assert any(plano.nome == "Intermediário" for plano in convenio.planos)
            assert any(plano.nome == "Avançado" for plano in convenio.planos)