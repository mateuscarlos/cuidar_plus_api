from typing import Optional, Dict, Any
from datetime import date
from pydantic import BaseModel, Field, EmailStr, validator
from src.infrastructure.utils.validators import validate_cpf

class UserCreateDTO(BaseModel):
    nome: str
    cpf: str
    email: EmailStr
    setor: str
    funcao: str
    password: str
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
    tipo_acesso: str = 'user'
    
    @validator('cpf')
    def cpf_must_be_valid(cls, v):
        if not validate_cpf(v):
            raise ValueError('CPF inválido')
        return v

class UserUpdateDTO(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    setor: Optional[str] = None
    funcao: Optional[str] = None
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
    status: Optional[str] = None
    tipo_acesso: Optional[str] = None

class UserResponseDTO(BaseModel):
    id: int
    nome: str
    cpf: str
    email: Optional[str]
    setor: str
    funcao: str
    status: str
    tipo_acesso: Optional[str]