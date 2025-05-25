from datetime import datetime
from db import db

class Plano(db.Model):
    __tablename__ = 'plano'
    
    id = db.Column(db.Integer, primary_key=True)
    convenio_id = db.Column(db.Integer, db.ForeignKey('convenio.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    tipo_acomodacao = db.Column(db.String(50), nullable=True)
    
    # Coberturas
    cobertura_ambulatorial = db.Column(db.Boolean, default=True)
    cobertura_hospitalar = db.Column(db.Boolean, default=True)
    cobertura_obstetrica = db.Column(db.Boolean, default=False)
    cobertura_odontologica = db.Column(db.Boolean, default=False)
    cobertura_emergencia = db.Column(db.Boolean, default=True)
    
    # Valores e carências
    valor_mensalidade = db.Column(db.Numeric(10, 2), nullable=True)
    carencia_consultas = db.Column(db.Integer, default=0)
    carencia_exames = db.Column(db.Integer, default=0)
    carencia_internacao = db.Column(db.Integer, default=0)
    
    # Observações e status
    observacoes = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    pacientes = db.relationship('Paciente', backref='plano', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'convenio_id': self.convenio_id,
            'nome': self.nome,
            'codigo': self.codigo,
            'descricao': self.descricao,
            'tipo_acomodacao': self.tipo_acomodacao,
            'cobertura_ambulatorial': self.cobertura_ambulatorial,
            'cobertura_hospitalar': self.cobertura_hospitalar,
            'cobertura_obstetrica': self.cobertura_obstetrica,
            'cobertura_odontologica': self.cobertura_odontologica,
            'cobertura_emergencia': self.cobertura_emergencia,
            'valor_mensalidade': float(self.valor_mensalidade) if self.valor_mensalidade else None,
            'carencia_consultas': self.carencia_consultas,
            'carencia_exames': self.carencia_exames,
            'carencia_internacao': self.carencia_internacao,
            'observacoes': self.observacoes,
            'ativo': self.ativo,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }