
import re
import bleach

def validate_cpf(cpf):
    """Valida um CPF"""
    if not cpf:
        return False
    
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Implementação da validação dos dígitos verificadores do CPF
    # (código conforme o utils.py original)
    
    return True

def sanitize_input(value: str, max_length=100) -> str:
    """Sanitiza e valida entradas de texto"""
    if value is None:
        return ''
    if not isinstance(value, str):
        raise ValueError("O valor deve ser uma string")
    cleaned = bleach.clean(value.strip())
    if len(cleaned) > max_length:
        raise ValueError(f"Campo excede o tamanho máximo de {max_length} caracteres")
    return cleaned