from datetime import datetime
from db import db
from utils import sanitize_input
from models.endereco import Endereco
from services.datetime_service import DateTimeService
import json

class Paciente(db.Model):
    __tablename__ = 'paciente'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date)
    cpf = db.Column(db.String(14), unique=True)
    genero = db.Column(db.String(20))
    estado_civil = db.Column(db.String(20))
    profissao = db.Column(db.String(50))
    nacionalidade = db.Column(db.String(50))
    endereco = db.Column(db.JSON, nullable=False)  # Armazena o endereço como JSON
    
    telefone = db.Column(db.String(20))
    telefone_secundario = db.Column(db.String(20))
    email = db.Column(db.String(100))
    contato_emergencia = db.Column(db.String(100))
    telefone_emergencia = db.Column(db.String(20))
    
    status = db.Column(db.String(20), default='ativo')
    cid_primario = db.Column(db.String(20))
    cid_secundario = db.Column(db.String(20))
    acomodacao = db.Column(db.String(50))
    medico_responsavel = db.Column(db.String(100))
    alergias = db.Column(db.Text)
    case_responsavel = db.Column(db.String(100))
    
    convenio_id = db.Column(db.String(50))
    plano_id = db.Column(db.String(50))
    numero_carteirinha = db.Column(db.String(50))
    data_validade = db.Column(db.Date)
    
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    @classmethod
    def from_json(cls, data):
        """Cria um objeto Paciente a partir de dados JSON"""
        processed_data = DateTimeService.process_form_data(data)
        
        paciente = cls(
            nome_completo=sanitize_input(processed_data.get('nome_completo', '')),
            cpf=sanitize_input(processed_data.get('cpf', '')),
            data_nascimento=processed_data.get('data_nascimento'),
            genero=sanitize_input(processed_data.get('genero', '')),
            estado_civil=sanitize_input(processed_data.get('estado_civil', '')),
            profissao=sanitize_input(processed_data.get('profissao', '')),
            nacionalidade=sanitize_input(processed_data.get('nacionalidade', '')),
            telefone=sanitize_input(processed_data.get('telefone', '')),
            telefone_secundario=sanitize_input(processed_data.get('telefone_secundario', '')),
            email=sanitize_input(processed_data.get('email', '')),
            contato_emergencia=sanitize_input(processed_data.get('contato_emergencia', '')),
            telefone_emergencia=sanitize_input(processed_data.get('telefone_emergencia', '')),
            status=sanitize_input(processed_data.get('status', 'ativo')),
            cid_primario=sanitize_input(processed_data.get('cid_primario', '')),
            cid_secundario=sanitize_input(processed_data.get('cid_secundario', '')),
            acomodacao=sanitize_input(processed_data.get('acomodacao', '')),
            medico_responsavel=sanitize_input(processed_data.get('medico_responsavel', '')),
            alergias=sanitize_input(processed_data.get('alergias', '')),
            case_responsavel=sanitize_input(processed_data.get('case_responsavel', '')),
            convenio_id=sanitize_input(processed_data.get('convenio_id', '')),
            plano_id=sanitize_input(processed_data.get('plano_id', '')),
            numero_carteirinha=sanitize_input(processed_data.get('numero_carteirinha', '')),
            data_validade=processed_data.get('data_validade'),
            endereco=Endereco.from_json(processed_data.get('endereco', {})) if processed_data.get('endereco') else None
        )
        
        return paciente
    
    def to_json(self):
        """Converte o objeto Paciente para JSON"""
        data = {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d') if self.data_nascimento else None,
            'genero': self.genero,
            'estado_civil': self.estado_civil,
            'profissao': self.profissao,
            'nacionalidade': self.nacionalidade,
            'telefone': self.telefone,
            'telefone_secundario': self.telefone_secundario,
            'email': self.email,
            'contato_emergencia': self.contato_emergencia,
            'telefone_emergencia': self.telefone_emergencia,
            'status': self.status,
            'cid_primario': self.cid_primario,
            'cid_secundario': self.cid_secundario,
            'acomodacao': self.acomodacao,
            'medico_responsavel': self.medico_responsavel,
            'alergias': self.alergias,
            'case_responsavel': self.case_responsavel,
            'convenio_id': self.convenio_id,
            'plano_id': self.plano_id,
            'numero_carteirinha': self.numero_carteirinha,
            'data_validade': self.data_validade.strftime('%Y-%m-%d') if self.data_validade else None,
            'endereco': self.endereco.to_json() if self.endereco else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
        
        return DateTimeService.format_model_to_response(data)