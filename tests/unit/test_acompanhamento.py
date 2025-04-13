import pytest
import sys
import os
import json
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app
from db import db
from models.acompanhamento import Acompanhamento
from models.pacientes import Paciente

class TestAcompanhamentoModel:
    """Testes para o modelo Acompanhamento"""
    
    def test_criar_acompanhamento_simples(self):
        """Testa a criação de um acompanhamento básico"""
        with app.app_context():
            # Criar um paciente primeiro
            paciente = Paciente(
                nome_completo="Paciente do Acompanhamento",
                cpf="12345678901",
                data_nascimento="1990-01-01",
                acomodacao="Apartamento",
                telefone="(11) 98765-4321",
                cid_primario="E11"
            )
            db.session.add(paciente)
            db.session.commit()
            
            # Criar acompanhamento
            data_atual = datetime.now()
            acompanhamento = Acompanhamento(
                paciente_id=paciente.id,
                data_hora=data_atual,
                tipo_atendimento="Consulta",
                motivo_atendimento="Avaliação inicial",
                descricao="Paciente relatou sintomas de gripe"
            )
            db.session.add(acompanhamento)
            db.session.commit()
            
            # Recuperar o acompanhamento do banco
            saved_acompanhamento = Acompanhamento.query.filter_by(paciente_id=paciente.id).first()
            
            # Verificações
            assert saved_acompanhamento is not None
            assert saved_acompanhamento.paciente_id == paciente.id
            assert saved_acompanhamento.tipo_atendimento == "Consulta"
            assert saved_acompanhamento.motivo_atendimento == "Avaliação inicial"
            assert saved_acompanhamento.descricao == "Paciente relatou sintomas de gripe"
            # Verificar se a data está próxima da atual (considerando segundos de diferença)
            assert abs((saved_acompanhamento.data_hora - data_atual).total_seconds()) < 5
    
    def test_acompanhamento_com_sinais_vitais(self):
        """Testa a criação de um acompanhamento com sinais vitais"""
        with app.app_context():
            # Criar um paciente
            paciente = Paciente(
                nome_completo="Paciente com Sinais Vitais",
                cpf="98765432109",
                data_nascimento="1985-05-15",
                acomodacao="Enfermaria",
                telefone="(11) 91234-5678",
                cid_primario="I10"
            )
            db.session.add(paciente)
            db.session.commit()
            
            # Criar acompanhamento com sinais vitais
            acompanhamento = Acompanhamento(
                paciente_id=paciente.id,
                data_hora=datetime.now(),
                tipo_atendimento="Visita",
                motivo_atendimento="Acompanhamento",
                descricao="Monitoramento dos sinais vitais"
            )
            
            # Adicionar sinais vitais
            acompanhamento.sinais_vitais = {
                "pressao_arterial": "120/80",
                "temperatura": 36.8,
                "frequencia_cardiaca": 75,
                "saturacao": 98
            }
            
            db.session.add(acompanhamento)
            db.session.commit()
            
            # Recuperar o acompanhamento do banco
            saved_acompanhamento = Acompanhamento.query.filter_by(paciente_id=paciente.id).first()
            
            # Verificações dos sinais vitais
            assert saved_acompanhamento.sinais_vitais is not None
            assert saved_acompanhamento.sinais_vitais["pressao_arterial"] == "120/80"
            assert saved_acompanhamento.sinais_vitais["temperatura"] == 36.8
            assert saved_acompanhamento.sinais_vitais["frequencia_cardiaca"] == 75
            assert saved_acompanhamento.sinais_vitais["saturacao"] == 98
    
    def test_acompanhamento_com_intervencoes(self):
        """Testa a criação de um acompanhamento com intervenções"""
        with app.app_context():
            # Criar um paciente
            paciente = Paciente(
                nome_completo="Paciente com Intervenções",
                cpf="55566677788",
                data_nascimento="1970-10-10",
                acomodacao="Apartamento",
                telefone="(11) 94567-8901",
                cid_primario="J45"
            )
            db.session.add(paciente)
            db.session.commit()
            
            # Criar acompanhamento com intervenções
            acompanhamento = Acompanhamento(
                paciente_id=paciente.id,
                data_hora=datetime.now(),
                tipo_atendimento="Procedimento",
                motivo_atendimento="Tratamento",
                descricao="Intervenções respiratórias"
            )
            
            # Adicionar intervenções
            acompanhamento.intervencoes = [
                {
                    "tipo": "Nebulização",
                    "medicamento": "Salbutamol",
                    "dosagem": "5mg",
                    "horario": datetime.now().strftime("%H:%M")
                },
                {
                    "tipo": "Oxigenoterapia",
                    "fluxo": "2L/min",
                    "duracao": "30 minutos"
                }
            ]
            
            db.session.add(acompanhamento)
            db.session.commit()
            
            # Recuperar o acompanhamento do banco
            saved_acompanhamento = Acompanhamento.query.filter_by(paciente_id=paciente.id).first()
            
            # Verificações das intervenções
            assert saved_acompanhamento.intervencoes is not None
            assert len(saved_acompanhamento.intervencoes) == 2
            assert saved_acompanhamento.intervencoes[0]["tipo"] == "Nebulização"
            assert saved_acompanhamento.intervencoes[0]["medicamento"] == "Salbutamol"
            assert saved_acompanhamento.intervencoes[1]["tipo"] == "Oxigenoterapia"
            assert saved_acompanhamento.intervencoes[1]["fluxo"] == "2L/min"
    
    def test_listar_acompanhamentos_por_paciente(self):
        """Testa a listagem de acompanhamentos de um paciente"""
        with app.app_context():
            # Criar um paciente
            paciente = Paciente(
                nome_completo="Paciente com Vários Acompanhamentos",
                cpf="11122233344",
                data_nascimento="1980-12-25",
                acomodacao="Apartamento",
                telefone="(11) 95555-6666",
                cid_primario="K29"
            )
            db.session.add(paciente)
            db.session.commit()
            
            # Criar múltiplos acompanhamentos para o paciente
            data_base = datetime.now()
            for i in range(3):
                acompanhamento = Acompanhamento(
                    paciente_id=paciente.id,
                    data_hora=data_base - timedelta(days=i),
                    tipo_atendimento=f"Tipo {i+1}",
                    motivo_atendimento=f"Motivo {i+1}",
                    descricao=f"Descrição {i+1}"
                )
                db.session.add(acompanhamento)
            
            db.session.commit()
            
            # Listar acompanhamentos do paciente
            acompanhamentos = Acompanhamento.query.filter_by(paciente_id=paciente.id).all()
            
            # Verificações
            assert len(acompanhamentos) == 3
            # Verificar se estão ordenados por data (mais recente primeiro)
            datas = [a.data_hora for a in acompanhamentos]
            assert datas[0] > datas[1] > datas[2]