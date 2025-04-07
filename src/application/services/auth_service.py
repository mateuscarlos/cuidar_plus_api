from typing import Tuple, Dict, Any, Optional
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.infrastructure.security.password_service import PasswordService
from src.infrastructure.security.token_service import TokenService
from src.application.dtos.user_dto import UserCreateDTO, UserResponseDTO

class AuthService:
    def __init__(
        self, 
        user_repository: UserRepositoryInterface, 
        password_service: PasswordService,
        token_service: TokenService
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.token_service = token_service
        
    def authenticate(self, email: str, password: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        """Autentica um usuário e retorna um token JWT"""
        user = self.user_repository.get_by_email(email)
        
        if not user:
            return None, None
            
        # Verificar senha
        if not self.password_service.verify_password(password, user.password_hash):
            return None, None
            
        # Gerar token JWT
        token = self.token_service.generate_token({
            'user_id': user.id,
            'email': user.email,
            'tipo_acesso': user.tipo_acesso
        })
        
        return token, UserResponseDTO.from_orm(user).dict()
        
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Registra um novo usuário"""
        return self._create_user(user_data)
        
    def _create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Método privado para criar um usuário"""
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