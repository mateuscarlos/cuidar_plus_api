import pytest
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app
from db import db
from models.convenio import Convenio
from models.plano import Plano

class TestConvenioModel:
    """Testes para o modelo Convenio"""
    
    def test_criar_convenio(self):
        """Testa a criação de um convênio"""
        with app.app_context():
            # Criar o convênio
            convenio = Convenio(nome="Convênio Teste Unitário")
            db.session.add(convenio)
            db.session.commit()
            
            # Recuperar o convênio do banco
            saved_convenio = Convenio.query.filter_by(nome="Convênio Teste Unitário").first()
            
            # Verificações
            assert saved_convenio is not None
            assert saved_convenio.nome == "Convênio Teste Unitário"
            assert saved_convenio.id > 0
    
    def test_atualizar_convenio(self):
        """Testa a atualização de um convênio"""
        with app.app_context():
            # Criar o convênio
            convenio = Convenio(nome="Nome Original")
            db.session.add(convenio)
            db.session.commit()
            
            # Atualizar o convênio
            convenio.nome = "Nome Atualizado"
            db.session.commit()
            
            # Recuperar o convênio atualizado
            updated_convenio = Convenio.query.get(convenio.id)
            
            # Verificações
            assert updated_convenio.nome == "Nome Atualizado"
    
    def test_excluir_convenio(self):
        """Testa a exclusão de um convênio"""
        with app.app_context():
            # Criar o convênio
            convenio = Convenio(nome="Convênio Para Excluir")
            db.session.add(convenio)
            db.session.commit()
            
            convenio_id = convenio.id
            
            # Excluir o convênio
            db.session.delete(convenio)
            db.session.commit()
            
            # Verificar que o convênio foi excluído
            deleted_convenio = Convenio.query.get(convenio_id)
            assert deleted_convenio is None

class TestPlanoModel:
    """Testes para o modelo Plano"""
    
    def test_criar_plano(self):
        """Testa a criação de um plano vinculado a um convênio"""
        with app.app_context():
            # Primeiro criar o convênio
            convenio = Convenio(nome="Convênio do Plano")
            db.session.add(convenio)
            db.session.commit()
            
            # Agora criar o plano
            plano = Plano(
                nome="Plano Teste",
                convenio_id=convenio.id
                # Remover 'cobertura' e 'carencia' que são inválidos
            )
            db.session.add(plano)
            db.session.commit()
            
            # Recuperar o plano do banco
            saved_plano = Plano.query.filter_by(nome="Plano Teste").first()
            
            # Verificações
            assert saved_plano is not None
            assert saved_plano.nome == "Plano Teste"
            assert saved_plano.convenio_id == convenio.id
    
    def test_relacao_plano_convenio(self):
        """Testa a relação entre plano e convênio"""
        with app.app_context():
            # Criar convênio
            convenio = Convenio(nome="Convênio Relação")
            db.session.add(convenio)
            db.session.commit()
            
            # Criar dois planos para o mesmo convênio
            plano1 = Plano(nome="Plano Básico", convenio_id=convenio.id)
            plano2 = Plano(nome="Plano Premium", convenio_id=convenio.id)
            db.session.add_all([plano1, plano2])
            db.session.commit()
            
            # Verificar a relação do lado do convênio
            assert len(convenio.planos) == 2
            assert any(p.nome == "Plano Básico" for p in convenio.planos)
            assert any(p.nome == "Plano Premium" for p in convenio.planos)
            
            # Verificar a relação do lado do plano
            assert plano1.convenio.nome == "Convênio Relação"
            assert plano2.convenio.nome == "Convênio Relação"