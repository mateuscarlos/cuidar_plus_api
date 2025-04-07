from dependency_injector import containers, providers
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security.password_service import PasswordService
from src.infrastructure.security.token_service import TokenService
from src.application.services.user_service import UserService
from src.application.services.auth_service import AuthService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["src.interfaces.api.routes"]
    )
    
    # Serviços de infraestrutura
    password_service = providers.Singleton(
        PasswordService
    )
    
    token_service = providers.Singleton(
        TokenService
    )
    
    # Repositórios
    user_repository = providers.Factory(
        UserRepository
    )
    
    # Serviços de aplicação
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        password_service=password_service
    )
    
    auth_service = providers.Factory(
        AuthService,
        user_repository=user_repository,
        password_service=password_service,
        token_service=token_service
    )

_container = None

def init_container():
    global _container
    _container = Container()
    return _container
    
def get_container():
    global _container
    if _container is None:
        _container = init_container()
    return _container