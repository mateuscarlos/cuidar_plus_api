import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models.convenio import Convenio
from models.plano import Plano
from app import app
from db import db

@pytest.fixture
def create_test_convenio():
    """Factory fixture para criar convênios de teste"""
    def _create_convenio(nome='Saúde Total', contato='(11) 3333-4444'):
        with app.app_context():
            convenio = Convenio(
                nome=nome,
                contato=contato
            )
            db.session.add(convenio)
            db.session.commit()
            return convenio
    return _create_convenio

@pytest.fixture
def create_test_plano(create_test_convenio):
    """Factory fixture para criar planos de teste"""
    def _create_plano(nome='Plano Premium', convenio_id=None):
        with app.app_context():
            if convenio_id is None:
                convenio = create_test_convenio()
                convenio_id = convenio.id
                
            plano = Plano(
                nome=nome,
                convenio_id=convenio_id
            )
            db.session.add(plano)
            db.session.commit()
            return plano
    return _create_plano

def test_criar_convenio(test_client):
    """Testa a criação de um novo convênio"""
    data = {
        'nome': 'Convênio Teste'
    }
    
    response = test_client.post('/convenios/criar', json=data)  # Rota correta
    
    assert response.status_code == 201
    result = json.loads(response.data)
    assert 'id' in result
    assert result['nome'] == 'Convênio Teste'

def test_listar_convenios(test_client, create_test_convenio):
    """Testa a listagem de convênios"""
    # Criar alguns convênios para teste
    create_test_convenio(nome='Convênio A')
    create_test_convenio(nome='Convênio B')
    
    response = test_client.get('/convenios')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 2