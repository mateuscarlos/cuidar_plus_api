import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from datetime import date
from models.pacientes import Paciente
from app import app
from db import db

@pytest.fixture
def create_test_paciente():
    """Factory fixture para criar pacientes de teste"""
    def _create_paciente(nome='José da Silva', cpf='12345678901', data_nascimento=date(1980, 1, 1)):
        with app.app_context():
            paciente = Paciente(
                nome_completo=nome,
                cpf=cpf,
                data_nascimento=data_nascimento,
                acomodacao='Apartamento',
                telefone='(11) 98765-4321',
                cid_primario='G40'
            )
            db.session.add(paciente)
            db.session.commit()
            return paciente
    return _create_paciente

def test_criar_paciente(test_client):
    """Testa a criação de um paciente"""
    dados_paciente = {
        'nome_completo': 'Fernanda Teste',
        'cpf': '11122233345',
        'data_nascimento': '15/05/1985',
        'acomodacao': 'Apartamento',
        'telefone': '(11) 98765-4321',
        'cid_primario': 'G40'
    }
    
    response = test_client.post('/pacientes/criar', json=dados_paciente)
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert 'id' in data
    assert data['nome_completo'] == 'Fernanda Teste'
    assert data['cpf'] == '11122233345'

def test_obter_paciente(test_client, create_test_paciente):
    """Testa a obtenção de um paciente específico"""
    # Criar um paciente para o teste
    with app.app_context():
        paciente = create_test_paciente(
            nome_completo="Paciente Específico", 
            cpf="44444444444"
        )
        
        # Fazer a requisição para obter o paciente
        response = test_client.get(f'/pacientes/{paciente.id}')
        
        # Verificar o resultado
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == paciente.id
        assert data['nome_completo'] == 'Paciente Específico'
        assert data['cpf'] == '44444444444'

def test_atualizar_paciente(test_client, create_test_paciente):
    """Testa a atualização de um paciente"""
    # Criar um paciente para o teste
    with app.app_context():
        paciente = create_test_paciente(
            nome_completo="Paciente Para Atualizar", 
            cpf="55555555555",
            telefone="(11) 99999-9999"
        )
        
        paciente_id = paciente.id  # Pegar o ID antes de encerrar o contexto
    
    # Dados para atualização
    dados_atualizacao = {
        'telefone': '(11) 88888-8888',
        'acomodacao': 'Enfermaria'
    }
    
    # Fazer a requisição para atualizar o paciente
    response = test_client.put(f'/pacientes/atualizar/{paciente_id}', json=dados_atualizacao)
    
    # Verificar o resultado
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == paciente_id
    assert data['telefone'] == '(11) 88888-8888'  # Atualizado
    assert data['acomodacao'] == 'Enfermaria'  # Atualizado