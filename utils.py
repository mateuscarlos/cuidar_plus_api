import re
import bleach

def validate_cpf(cpf: str) -> bool:
    """Valida o formato e dígitos verificadores do CPF"""
    cpf = re.sub(r'[^\d]', '', cpf)
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    def calculate_digit(cpf, length):
        soma = sum(int(cpf[i]) * (length - i) for i in range(length - 1))
        resto = (soma * 10) % 11
        return resto if resto < 10 else 0
    
    digito1 = calculate_digit(cpf, 10)
    digito2 = calculate_digit(cpf, 11)
    
    return cpf[-2:] == f"{digito1}{digito2}"

def sanitize_input(value: str, max_length=100) -> str:
    """Sanitiza e valida entradas de texto"""
    if value is None:
        return ''
    cleaned = bleach.clean(value.strip())
    if len(cleaned) > max_length:
        raise ValueError(f"Campo excede o tamanho máximo de {max_length} caracteres")
    return cleaned
