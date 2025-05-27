"""
Utilitários para gerenciamento de senhas
"""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, HashingError
import re
import logging

logger = logging.getLogger(__name__)

class PasswordManager:
    def __init__(self):
        # Configurações do Argon2 para produção
        self.ph = PasswordHasher(
            time_cost=2,      # Número de iterações
            memory_cost=65536, # Memória em KB (64MB)
            parallelism=1,    # Número de threads
            hash_len=32,      # Tamanho do hash
            salt_len=16       # Tamanho do salt
        )
    
    def hash_password(self, password: str) -> str:
        """
        Cria um hash da senha usando Argon2
        """
        try:
            if not password:
                raise ValueError("Senha não pode estar vazia")
            
            return self.ph.hash(password)
        except HashingError as e:
            logger.error(f"Erro ao criar hash da senha: {e}")
            raise
    
    def verify_password(self, password_hash: str, password: str) -> bool:
        """
        Verifica se a senha corresponde ao hash
        """
        try:
            self.ph.verify(password_hash, password)
            return True
        except VerifyMismatchError:
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar senha: {e}")
            return False
    
    def needs_rehash(self, password_hash: str) -> bool:
        """
        Verifica se o hash precisa ser atualizado
        """
        try:
            return self.ph.check_needs_rehash(password_hash)
        except Exception as e:
            logger.error(f"Erro ao verificar necessidade de rehash: {e}")
            return False
    
    def validate_password_strength(self, password: str) -> dict:
        """
        Valida a força da senha
        """
        result = {
            'valid': False,
            'errors': []
        }
        
        if len(password) < 8:
            result['errors'].append('A senha deve ter pelo menos 8 caracteres')
        
        if not re.search(r'[a-z]', password):
            result['errors'].append('A senha deve conter pelo menos uma letra minúscula')
        
        if not re.search(r'[A-Z]', password):
            result['errors'].append('A senha deve conter pelo menos uma letra maiúscula')
        
        if not re.search(r'\d', password):
            result['errors'].append('A senha deve conter pelo menos um número')
        
        if not re.search(r'[@$!%*?&]', password):
            result['errors'].append('A senha deve conter pelo menos um caractere especial (@$!%*?&)')
        
        result['valid'] = len(result['errors']) == 0
        return result

# Instância global
password_manager = PasswordManager()