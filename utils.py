import re
import bleach
from datetime import datetime
import pytz
import requests
from werkzeug.exceptions import BadRequest

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
    if not isinstance(value, str):
        raise ValueError("O valor deve ser uma string")
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

def get_address_from_cep(cep):
    """
    Obtém o endereço a partir do CEP usando a API ViaCEP.
    
    :param cep: CEP do usuário
    :return: dados do endereço
    """
    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    if response.status_code != 200:
        raise BadRequest("CEP inválido")
    data = response.json()
    if 'erro' in data:
        raise BadRequest("CEP inválido")
    return data

def convert_utc_to_db_format(utc_date_str):
    """
    Converte uma string de data UTC para o formato do banco de dados.
    
    :param utc_date_str: string de data em UTC (ex: '2025-03-13T12:00:00Z')
    :return: string de data no formato do banco de dados (ex: '2025-03-13 12:00:00')
    """
    utc_date = datetime.strptime(utc_date_str, '%Y-%m-%dT%H:%M:%SZ')
    return utc_date.strftime('%Y-%m-%d %H:%M:%S')

def convert_ddmmyyyy_to_db_format(date_str):
    """
    Converte uma string de data para o formato do banco de dados (YYYY-MM-DD).
    Aceita tanto o formato DD/MM/YYYY quanto YYYY-MM-DD.
    
    :param date_str: string de data no formato dd/mm/yyyy ou yyyy-mm-dd
    :return: string de data no formato do banco de dados (ex: '2025-03-13')
    """
    if not date_str:
        return None
        
    # Verifica se a data já está no formato YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str
    
    # Verifica se a data está no formato DD/MM/YYYY
    elif re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
        try:
            date = datetime.strptime(date_str, '%d/%m/%Y')
            return date.strftime('%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Formato de data inválido: {date_str}. Use DD/MM/YYYY ou YYYY-MM-DD.")
    else:
        raise ValueError(f"Formato de data inválido: {date_str}. Use DD/MM/YYYY ou YYYY-MM-DD.")

def format_date(date_string, output_format='iso'):
    """
    Formata uma string de data entre diferentes formatos
    
    Args:
        date_string (str): Data em formato string (DD/MM/YYYY ou YYYY-MM-DD)
        output_format (str): Formato desejado ('iso' ou 'br')
    
    Returns:
        str: Data formatada no formato especificado
    """
    if output_format == 'iso':
        # Converte formato brasileiro (DD/MM/YYYY) para ISO (YYYY-MM-DD)
        if '/' in date_string:
            day, month, year = date_string.split('/')
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        return date_string
    elif output_format == 'br':
        # Converte formato ISO (YYYY-MM-DD) para brasileiro (DD/MM/YYYY)
        if '-' in date_string:
            year, month, day = date_string.split('-')
            return f"{day}/{month}/{year}"
        return date_string
    else:
        return date_string