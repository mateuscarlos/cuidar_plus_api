from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.domain.entities.user import UserEntity

class UserRepositoryInterface(ABC):
    @abstractmethod
    def create(self, user_data: Dict[str, Any]) -> UserEntity:
        """Cria um novo usuário"""
        pass
        
    @abstractmethod
    def get_all(self) -> List[UserEntity]:
        """Retorna todos os usuários"""
        pass
        
    @abstractmethod
    def get_by_cpf(self, cpf: str) -> Optional[UserEntity]:
        """Busca um usuário pelo CPF"""
        pass
        
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Busca um usuário pelo email"""
        pass
        
    @abstractmethod
    def update(self, cpf: str, user_data: Dict[str, Any]) -> Optional[UserEntity]:
        """Atualiza um usuário pelo CPF"""
        pass
        
    @abstractmethod
    def delete(self, cpf: str) -> bool:
        """Remove um usuário pelo CPF"""
        pass