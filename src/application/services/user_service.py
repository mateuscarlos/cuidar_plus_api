
from typing import List, Dict, Any, Optional
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.application.dtos.user_dto import UserCreateDTO, UserUpdateDTO, UserResponseDTO
from src.infrastructure.security.password_service import PasswordService

class UserService:
    def __init__(self, user_repository: UserRepositoryInterface, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service
        
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo usuário"""
        # Validar dados com DTO
        user_dto = UserCreateDTO(**user_data)
        
        # Verificar se usuário já existe
        existing_user = self.user_repository.get_by_cpf(user_dto.cpf)
        if existing_user:
            raise ValueError(f"Usuário com CPF {user_dto.cpf} já existe")
            
        existing_email = self.user_repository.get_by_email(user_dto.email)
        if existing_email:
            raise ValueError(f"Email {user_dto.email} já está em uso")
            
        # Hash da senha
        user_data['password_hash'] = self.password_service.hash_password(user_dto.password)
        del user_data['password']
        
        # Criar usuário
        user = self.user_repository.create(user_data)
        
        # Retornar dados formatados
        return UserResponseDTO.from_orm(user).dict()
        
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Retorna todos os usuários"""
        users = self.user_repository.get_all()
        return [UserResponseDTO.from_orm(user).dict() for user in users]
        
    def get_user_by_cpf(self, cpf: str) -> Optional[Dict[str, Any]]:
        """Busca um usuário pelo CPF"""
        user = self.user_repository.get_by_cpf(cpf)
        if not user:
            return None
        return UserResponseDTO.from_orm(user).dict()
        
    def update_user(self, cpf: str, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Atualiza um usuário pelo CPF"""
        # Validar dados com DTO
        user_update_dto = UserUpdateDTO(**user_data)
        
        # Atualizar usuário
        updated_user = self.user_repository.update(cpf, user_update_dto.dict(exclude_none=True))
        if not updated_user:
            raise ValueError(f"Usuário com CPF {cpf} não encontrado")
            
        return UserResponseDTO.from_orm(updated_user).dict()
        
    def delete_user(self, cpf: str) -> bool:
        """Remove um usuário pelo CPF"""
        result = self.user_repository.delete(cpf)
        if not result:
            raise ValueError(f"Usuário com CPF {cpf} não encontrado")
        return True