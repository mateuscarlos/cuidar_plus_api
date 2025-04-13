import pytest
import json
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from datetime import date
from models.pacientes import Paciente
from models.acompanhamento import Acompanhamento
from app import app
from db import db

@pytest.fixture
def create_test_paciente_e_acompanhamento():
    """Factory fixture para criar paciente e acompanhamento de teste"""
    def _create():
        with app.app_context():
            # Cria o paciente
            paciente = Paciente(
                nome_completo='Roberto Acompanhamento',
                cpf='55566677788',
                data_nascimento=date(1970, 10, 20),
                acomodacao='Apartamento',
                telefone='(11) 98888-7777',
                cid_primario='I10'
            )
            db.session.add(paciente)
            db.session.commit()
            
            # Cria o acompanhamento
            acompanhamento = Acompanhamento(
                paciente_id=paciente.id,
                data_hora=date(2025, 4, 10),
                tipo_atendimento='Visita',
                motivo_atendimento='Avaliação periódica',
                descricao='Paciente apresentou melhora'
            )
            db.session.add(acompanhamento)
            db.session.commit()
            
            return {'paciente': paciente, 'acompanhamento': acompanhamento}
    return _create

# Atualizando apenas os endpoints para testes de acompanhamentos

def test_criar_acompanhamento(test_client, create_test_paciente):
    """Testa a criação de um novo acompanhamento"""
    # Criar um paciente para o teste
    paciente = create_test_paciente(
        nome_completo="Paciente do Acompanhamento",
        cpf="12312312312"
    )
    
    # Dados do acompanhamento
    dados_acompanhamento = {
        'paciente_id': paciente.id,
        'tipo_atendimento': 'Consulta',
        'motivo_atendimento': 'Avaliação inicial',
        'descricao_motivo': 'Paciente com queixas de dor de cabeça',
        'sinais_vitais': {
            'pressao_arterial': '120/80',
            'temperatura': 36.5,
            'saturacao': 97
        }
    }
    
    # Fazer a requisição para criar o acompanhamento
    response = test_client.post('/acompanhamentos', json=dados_acompanhamento)
    
    # Verificar o resultado
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['paciente_id'] == paciente.id
    assert data['tipo_atendimento'] == 'Consulta'
    
    # Verificar que os dados JSON foram salvos corretamente
    sinais_vitais = data.get('sinais_vitais')
    assert sinais_vitais is not None
    assert sinais_vitais['temperatura'] == 36.5

def test_obter_acompanhamentos_por_paciente(test_client, create_test_paciente, create_test_acompanhamento):
    """Testa a listagem de acompanhamentos de um paciente"""
    # Criar um paciente para o teste
    paciente = create_test_paciente(
        nome_completo="Paciente com Acompanhamentos",
        cpf="45645645645"
    )
    
    # Criar alguns acompanhamentos para o paciente
    for i in range(3):
        create_test_acompanhamento(
            paciente=paciente,
            tipo_atendimento=f"Tipo {i+1}",
            motivo_atendimento=f"Motivo {i+1}",
            descricao=f"Descrição {i+1}"
        )
    
    # Fazer a requisição para listar os acompanhamentos
    response = test_client.get(f'/acompanhamentos/paciente/{paciente.id}')
    
    # Verificar o resultado
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 3

def test_obter_acompanhamento_especifico(test_client, create_test_paciente, create_test_acompanhamento):
    """Testa a obtenção de um acompanhamento específico"""
    # Criar um paciente e um acompanhamento para o teste
    paciente = create_test_paciente(
        nome_completo="Paciente Específico",
        cpf="78978978978"
    )
    
    acompanhamento = create_test_acompanhamento(
        paciente=paciente,
        tipo_atendimento="Visita",
        motivo_atendimento="Reavaliação",
        descricao="Paciente com melhora dos sintomas"
    )
    
    # Fazer a requisição para obter o acompanhamento
    response = test_client.get(f'/acompanhamentos/{acompanhamento.id}')
    
    # Verificar o resultado
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == acompanhamento.id
    assert data['paciente_id'] == paciente.id
    assert data['tipo_atendimento'] == "Visita"
    assert data['motivo_atendimento'] == "Reavaliação"

def test_atualizar_acompanhamento(test_client, create_test_paciente, create_test_acompanhamento):
    """Testa a atualização de um acompanhamento"""
    # Criar um paciente e um acompanhamento para o teste
    paciente = create_test_paciente(
        nome_completo="Paciente para Atualizar",
        cpf="01010101010"
    )
    
    acompanhamento = create_test_acompanhamento(
        paciente=paciente,
        tipo_atendimento="Visita Inicial",
        motivo_atendimento="Avaliação",
        descricao="Primeira avaliação"
    )
    
    # Dados para atualização
    dados_atualizacao = {
        'tipo_atendimento': 'Visita de Retorno',
        'descricao': 'Reavaliação após tratamento',
        'sinais_vitais': {
            'pressao_arterial': '110/70',
            'temperatura': 36.2,
            'saturacao': 99
        }
    }
    
    # Fazer a requisição para atualizar o acompanhamento
    response = test_client.put(f'/acompanhamentos/{acompanhamento.id}', json=dados_atualizacao)
    
    # Verificar o resultado
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == acompanhamento.id
    assert data['tipo_atendimento'] == 'Visita de Retorno'
    assert data['descricao'] == 'Reavaliação após tratamento'
    assert data['sinais_vitais']['temperatura'] == 36.2