from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class UserEntity:
    nome: str
    cpf: str
    setor: str
    funcao: str
    id: Optional[int] = None
    email: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    cep: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    especialidade: Optional[str] = None
    registro_categoria: Optional[str] = None
    telefone: Optional[str] = None
    data_admissao: Optional[date] = None
    status: str = 'Ativo'
    tipo_acesso: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None