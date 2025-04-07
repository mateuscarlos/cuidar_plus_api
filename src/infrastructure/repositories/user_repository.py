from typing import List, Optional, Dict, Any
from datetime import datetime
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.domain.entities.user import UserEntity
from src.infrastructure.database.models.user import User
from src.infrastructure.database.db_config import db

class UserRepository(UserRepositoryInterface):
    def create(self, user_data: Dict[str, Any]) -> UserEntity:
        """Cria um novo usuário"""
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return self._map_to_entity(user)
        
    def get_all(self) -> List[UserEntity]:
        """Retorna todos os usuários"""
        users = User.query.all()
        return [self._map_to_entity(user) for user in users]
        
    def get_by_cpf(self, cpf: str) -> Optional[UserEntity]:
        """Busca um usuário pelo CPF"""
        user = User.query.filter_by(cpf=cpf).first()
        if not user:
            return None
        return self._map_to_entity(user)
        
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Busca um usuário pelo email"""
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        return self._map_to_entity(user)
        
    def update(self, cpf: str, user_data: Dict[str, Any]) -> Optional[UserEntity]:
        """Atualiza um usuário pelo CPF"""
        user = User.query.filter_by(cpf=cpf).first()
        if not user:
            return None
            
        for key, value in user_data.items():
            setattr(user, key, value)
            
        user.updated_at = datetime.utcnow()
        db.session.commit()
        return self._map_to_entity(user)
        
    def delete(self, cpf: str) -> bool:
        """Remove um usuário pelo CPF"""
        user = User.query.filter_by(cpf=cpf).first()
        if not user:
            return False
            
        db.session.delete(user)
        db.session.commit()
        return True
        
    def _map_to_entity(self, model: User) -> UserEntity:
        """Mapeia um modelo ORM para uma entidade de domínio"""
        return UserEntity(
            id=model.id,
            nome=model.nome,
            cpf=model.cpf,
            email=model.email,
            rua=model.rua,
            numero=model.numero,
            complemento=model.complemento,
            cep=model.cep,
            bairro=model.bairro,
            cidade=model.cidade,
            estado=model.estado,
            setor=model.setor,
            funcao=model.funcao,
            especialidade=model.especialidade,
            registro_categoria=model.registro_categoria,
            telefone=model.telefone,
            data_admissao=model.data_admissao,
            status=model.status,
            tipo_acesso=model.tipo_acesso,
            created_at=model.created_at,
            updated_at=model.updated_at
        )