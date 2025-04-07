import pytz
from datetime import datetime

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