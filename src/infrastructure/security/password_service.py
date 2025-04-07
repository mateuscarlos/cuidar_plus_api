from werkzeug.security import generate_password_hash, check_password_hash

class PasswordService:
    def hash_password(self, password: str) -> str:
        """Gera um hash de senha seguro"""
        return generate_password_hash(password)
        
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verifica se a senha corresponde ao hash"""
        return check_password_hash(password_hash, password)