import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import json
from src.interfaces.api.app import app
from infrastructure.database.db_config import db
from models.user import User

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/test_cuidar_plus_api'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()
        print("Banco de dados de teste criado com sucesso.")
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()

@pytest.fixture(autouse=True)
def clear_db():
    with app.app_context():
        db.session.query(User).delete()
        db.session.commit()

def test_create_user(test_client):
    response = test_client.post('/api/criar_usuario', json={
        'nome': 'João da Silva',
        'cpf': '12345678909',
        'setor': 'TI',
        'funcao': 'Desenvolvedor'
    })
    assert response.status_code == 201
    assert 'Usuário criado com sucesso!' in response.get_json()['message']

def test_create_user_missing_fields(test_client):
    response = test_client.post('/api/criar_usuario', json={
        'nome': 'João da Silva',
        'cpf': '12345678909'
    })
    assert response.status_code == 400
    assert 'Campos obrigatórios faltando' in response.get_json()['message']

def test_get_all_users(test_client):
    with app.app_context():
        user = User(nome='João da Silva', cpf='12345678909', setor='TI', funcao='Desenvolvedor')
        db.session.add(user)
        db.session.commit()
    response = test_client.get('/api/exibe_usuarios')
    assert response.status_code == 200
    assert len(response.get_json()['usuarios']) == 1

def test_update_user(test_client):
    with app.app_context():
        user = User(nome='João da Silva', cpf='12345678909', setor='TI', funcao='Desenvolvedor')
        db.session.add(user)
        db.session.commit()
    response = test_client.put('/api/atualizar_usuario/12345678909', json={
        'nome': 'João da Silva Updated'
    })
    assert response.status_code == 200
    assert 'Usuário atualizado com sucesso!' in response.get_json()['message']

def test_delete_user(test_client):
    with app.app_context():
        user = User(nome='João da Silva', cpf='12345678909', setor='TI', funcao='Desenvolvedor')
        db.session.add(user)
        db.session.commit()
    response = test_client.delete('/api/excluir_usuario/12345678909')
    assert response.status_code == 200
    assert 'Usuário excluído com sucesso!' in response.get_json()['message']

def test_functional_create_user(test_client):
    response = test_client.post('/api/criar_usuario', json={
        'nome': 'Maria da Silva',
        'cpf': '98765432100',
        'setor': 'RH',
        'funcao': 'Analista'
    })
    assert response.status_code == 201
    assert 'Usuário criado com sucesso!' in response.get_json()['message']

def test_functional_get_all_users(test_client):
    with app.app_context():
        user1 = User(nome='João da Silva', cpf='12345678909', setor='TI', funcao='Desenvolvedor')
        user2 = User(nome='Maria da Silva', cpf='98765432100', setor='RH', funcao='Analista')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
    response = test_client.get('/api/exibe_usuarios')
    assert response.status_code == 200
    assert len(response.get_json()['usuarios']) == 2

def test_functional_update_user(test_client):
    with app.app_context():
        user = User(nome='João da Silva', cpf='12345678909', setor='TI', funcao='Desenvolvedor')
        db.session.add(user)
        db.session.commit()
    response = test_client.put('/api/atualizar_usuario/12345678909', json={
        'nome': 'João da Silva Updated'
    })
    assert response.status_code == 200
    assert 'Usuário atualizado com sucesso!' in response.get_json()['message']

def test_functional_delete_user(test_client):
    with app.app_context():
        user = User(nome='João da Silva', cpf='12345678909', setor='TI', funcao='Desenvolvedor')
        db.session.add(user)
        db.session.commit()
    response = test_client.delete('/api/excluir_usuario/12345678909')
    assert response.status_code == 200
    assert 'Usuário excluído com sucesso!' in response.get_json()['message']

def test_example(test_client):
    # Adicione um log para verificar o estado inicial do banco de dados
    with app.app_context():
        user = User(nome='João da Silva', cpf='12345678909', setor='TI', funcao='Desenvolvedor')
        db.session.add(user)
        db.session.commit()
        users = User.query.all()
        print(f"Usuários no banco de dados antes do teste: {users}")

    # Exemplo de teste
    response = test_client.get('/api/exibe_usuarios')
    print(f"Response status code: {response.status_code}")
    assert response.status_code == 200

    # Adicione um log para verificar o estado final do banco de dados
    with app.app_context():
        users = User.query.all()
        print(f"Usuários no banco de dados após o teste: {users}")