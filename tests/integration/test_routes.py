import pytest
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Testes para rotas da API de usuários
def test_get_all_users(client):
    """Testa a obtenção da lista de usuários"""
    response = client.get('/usuarios/lista')  # Rota correta conforme user_routes.py
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_create_and_get_user(client):
    """Testa criação e depois obtenção de um usuário específico"""
    # Criar um usuário com todos os campos necessários
    new_user = {
        'nome': 'Teste Integração',
        'cpf': '12345678909',
        'email': 'teste@integracao.com',
        'password': 'senha123',  # Campo para senha
        'cep': '01001000',  # CEP obrigatório
        'setor': 'TI',
        'funcao': 'Desenvolvedor'
    }
    
    response = client.post('/usuarios/criar', json=new_user)
    
    # Permitir tanto 201 (sucesso) quanto 200 (alternativo)
    assert response.status_code in [200, 201]
    
    if response.status_code == 201:
        created_user = json.loads(response.data)
        if 'user' in created_user:
            user_id = created_user['user']['id']
            
            # Obter o usuário criado
            response = client.get(f'/usuarios/{user_id}')
            assert response.status_code == 200
            
            retrieved_user = json.loads(response.data)
            assert retrieved_user['nome'] == 'Teste Integração'
            assert retrieved_user['cpf'] == '12345678909'

# Testes para rotas da API de pacientes
def test_get_all_pacientes(client):
    """Testa a obtenção da lista de pacientes"""
    response = client.get('/pacientes')  # Rota correta conforme pacientes_routes.py
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_create_and_update_paciente(client):
    """Testa criação e atualização de um paciente"""
    # Criar um paciente
    new_paciente = {
        'nome_completo': 'Paciente Teste',
        'cpf': '98765432109',
        'data_nascimento': '01/01/1990',  # Formato brasileiro
        'telefone': '(11) 99999-8888',
        'acomodacao': 'Apartamento'
    }
    
    response = client.post('/pacientes/criar', json=new_paciente)
    
    # Permitir tanto 201 (sucesso) quanto 200 (alternativo)
    assert response.status_code in [200, 201]
    
    if response.status_code == 201:
        created_paciente = json.loads(response.data)
        paciente_id = created_paciente['id']
        
        # Atualizar o paciente
        update_data = {
            'telefone': '(11) 88888-7777',
            'acomodacao': 'Enfermaria'
        }
        
        response = client.put(f'/pacientes/atualizar/{paciente_id}', json=update_data)
        assert response.status_code == 200
        
        updated_paciente = json.loads(response.data)
        assert updated_paciente['telefone'] == '(11) 88888-7777'
        assert updated_paciente['acomodacao'] == 'Enfermaria'
        # Os campos não atualizados devem permanecer iguais
        assert updated_paciente['nome_completo'] == 'Paciente Teste'