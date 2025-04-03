from datetime import datetime
from db import db
from utils import convert_utc_to_db_format, convert_ddmmyyyy_to_db_format
from models.endereco import Endereco
import json

class Paciente(db.Model):
    __tablename__ = 'paciente'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    convenio_id = db.Column(db.Integer, db.ForeignKey('convenio.id', ondelete='SET NULL'), nullable=True)
    plano_id = db.Column(db.Integer, db.ForeignKey('plano.id', ondelete='SET NULL'), nullable=True)
    numero_carteirinha = db.Column(db.String(50), nullable=True)
    acomodacao = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    telefone_secundario = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    alergias = db.Column(db.Text, nullable=True)
    cid_primario = db.Column(db.String(10), nullable=False)
    cid_secundario = db.Column(db.String(10), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=False)
    endereco_json = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='em-avaliacao')
    genero = db.Column(db.String(20), nullable=True)
    estado_civil = db.Column(db.String(20), nullable=True)
    profissao = db.Column(db.String(50), nullable=True)
    nacionalidade = db.Column(db.String(50), nullable=True, default='Brasileiro(a)')
    data_validade = db.Column(db.Date, nullable=True)
    contato_emergencia = db.Column(db.String(100), nullable=True)
    telefone_emergencia = db.Column(db.String(15), nullable=True)
    case_responsavel = db.Column(db.String(100), nullable=True)
    medico_responsavel = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    acompanhamentos = db.relationship('Acompanhamento', backref='paciente', lazy=True, cascade="all, delete-orphan")

    @property
    def endereco(self):
        """Retorna o objeto Endereco a partir do JSON armazenado"""
        return Endereco.from_json(self.endereco_json)
    
    @endereco.setter
    def endereco(self, endereco):
        """Define o JSON do endereço a partir de um objeto Endereco"""
        if endereco is None:
            self.endereco_json = None
        else:
            self.endereco_json = endereco.to_json()
    
    def to_dict(self):
        endereco_dict = self.endereco.to_dict() if self.endereco else {}
        
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'cpf': self.cpf,
            'convenio_id': self.convenio_id,
            'plano_id': self.plano_id,
            'numero_carteirinha': self.numero_carteirinha,
            'acomodacao': self.acomodacao,
            'telefone': self.telefone,
            'telefone_secundario': self.telefone_secundario,
            'email': self.email,
            'alergias': self.alergias,
            'cid_primario': self.cid_primario,
            'cid_secundario': self.cid_secundario,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d') if self.data_nascimento else None,
            'endereco': self.endereco_json,
            'status': self.status,
            'genero': self.genero,
            'estado_civil': self.estado_civil,
            'profissao': self.profissao,
            'nacionalidade': self.nacionalidade,
            'data_validade': self.data_validade.strftime('%Y-%m-%d') if self.data_validade else None,
            'contato_emergencia': self.contato_emergencia,
            'telefone_emergencia': self.telefone_emergencia,
            'case_responsavel': self.case_responsavel,
            'medico_responsavel': self.medico_responsavel,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria um objeto Paciente a partir de um dicionário"""
        paciente = cls(
            nome_completo=data.get('nome_completo'),
            cpf=data.get('cpf'),
            data_nascimento=datetime.strptime(data.get('data_nascimento'), '%Y-%m-%d'),
            genero=data.get('genero'),
            estado_civil=data.get('estado_civil'),
            profissao=data.get('profissao'),
            nacionalidade=data.get('nacionalidade'),
            telefone=data.get('telefone'),
            telefone_secundario=data.get('telefone_secundario'),
            email=data.get('email'),
            status=data.get('status', 'em-avaliacao'),
            cid_primario=data.get('cid_primario'),
            cid_secundario=data.get('cid_secundario'),
            acomodacao=data.get('acomodacao'),
            medico_responsavel=data.get('medico_responsavel'),
            alergias=data.get('alergias'),
            convenio_id=data.get('convenio_id'),
            plano_id=data.get('plano_id'),
            numero_carteirinha=data.get('numero_carteirinha'),
            data_validade=datetime.strptime(data.get('data_validade'), '%Y-%m-%d') if data.get('data_validade') else None,
            contato_emergencia=data.get('contato_emergencia'),
            telefone_emergencia=data.get('telefone_emergencia'),
            case_responsavel=data.get('case_responsavel'),
        )

        # Processar o endereço
        if data.get('endereco'):
            endereco_data = data.get('endereco')
            endereco_data['rua'] = endereco_data.pop('logradouro', None)  # Mapear 'logradouro' para 'rua'
            paciente.endereco = Endereco.from_dict(endereco_data)

        return paciente