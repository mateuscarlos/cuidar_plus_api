import re
import bleach
from datetime import datetime
import pytz

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

def get_local_time(utc_dt, timezone_str):
    """
    Converte a data e hora UTC para o fuso horário local do usuário.
    
    :param utc_dt: datetime em UTC
    :param timezone_str: string do fuso horário (ex: 'America/Sao_Paulo')
    :return: datetime no fuso horário local
    """
    local_tz = pytz.timezone(timezone_str)
    local_dt = utc_dt.astimezone(local_tz)
    return local_dt


import requests

def get_user_timezone(ip_address):
    """
    Obtém o fuso horário do usuário com base no endereço IP.
    
    :param ip_address: Endereço IP do usuário
    :return: string do fuso horário (ex: 'America/Sao_Paulo')
    """
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}')
        response.raise_for_status()
        data = response.json()
        return data.get('timezone', 'UTC')
    except requests.RequestException:
        return 'UTC'