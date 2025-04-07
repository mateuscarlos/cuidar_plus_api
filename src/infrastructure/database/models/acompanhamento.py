from datetime import datetime
from infrastructure.database.db_config import db
import json

class Acompanhamento(db.Model):
    __tablename__ = 'acompanhamento'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    tipo_atendimento = db.Column(db.String(50), nullable=False)
    motivo_atendimento = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    
    # Dados JSON para estruturas complexas
    sinais_vitais_json = db.Column(db.Text, nullable=True)
    avaliacao_feridas_json = db.Column(db.Text, nullable=True)
    avaliacao_dispositivos_json = db.Column(db.Text, nullable=True)
    intervencoes_json = db.Column(db.Text, nullable=True)
    plano_acao_json = db.Column(db.Text, nullable=True)
    comunicacao_json = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Getters e setters para os campos JSON
    @property
    def sinais_vitais(self):
        if not self.sinais_vitais_json:
            return None
        return json.loads(self.sinais_vitais_json)
    
    @sinais_vitais.setter
    def sinais_vitais(self, value):
        if value is None:
            self.sinais_vitais_json = None
        else:
            self.sinais_vitais_json = json.dumps(value)
    
    @property
    def avaliacao_feridas(self):
        if not self.avaliacao_feridas_json:
            return None
        return json.loads(self.avaliacao_feridas_json)
    
    @avaliacao_feridas.setter
    def avaliacao_feridas(self, value):
        if value is None:
            self.avaliacao_feridas_json = None
        else:
            self.avaliacao_feridas_json = json.dumps(value)
    
    @property
    def avaliacao_dispositivos(self):
        if not self.avaliacao_dispositivos_json:
            return None
        return json.loads(self.avaliacao_dispositivos_json)
    
    @avaliacao_dispositivos.setter
    def avaliacao_dispositivos(self, value):
        if value is None:
            self.avaliacao_dispositivos_json = None
        else:
            self.avaliacao_dispositivos_json = json.dumps(value)
    
    @property
    def intervencoes(self):
        if not self.intervencoes_json:
            return None
        return json.loads(self.intervencoes_json)
    
    @intervencoes.setter
    def intervencoes(self, value):
        if value is None:
            self.intervencoes_json = None
        else:
            self.intervencoes_json = json.dumps(value)
    
    @property
    def plano_acao(self):
        if not self.plano_acao_json:
            return None
        return json.loads(self.plano_acao_json)
    
    @plano_acao.setter
    def plano_acao(self, value):
        if value is None:
            self.plano_acao_json = None
        else:
            self.plano_acao_json = json.dumps(value)
    
    @property
    def comunicacao(self):
        if not self.comunicacao_json:
            return None
        return json.loads(self.comunicacao_json)
    
    @comunicacao.setter
    def comunicacao(self, value):
        if value is None:
            self.comunicacao_json = None
        else:
            self.comunicacao_json = json.dumps(value)
    
    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'data_hora': self.data_hora.strftime('%Y-%m-%d %H:%M:%S') if self.data_hora else None,
            'tipo_atendimento': self.tipo_atendimento,
            'motivo_atendimento': self.motivo_atendimento,
            'descricao': self.descricao,
            'sinais_vitais': self.sinais_vitais,
            'avaliacao_feridas': self.avaliacao_feridas,
            'avaliacao_dispositivos': self.avaliacao_dispositivos,
            'intervencoes': self.intervencoes,
            'plano_acao': self.plano_acao,
            'comunicacao': self.comunicacao,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }