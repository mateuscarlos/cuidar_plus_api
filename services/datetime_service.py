import re
from datetime import datetime, timedelta
import pytz
from typing import Optional, Union, Dict, Any

class DateTimeService:
    """
    Serviço para tratamento de datas e horas no padrão brasileiro,
    garantindo consistência na timezone (America/Sao_Paulo)
    """
    
    # Timezone padrão para o Brasil/São Paulo
    TIMEZONE = pytz.timezone('America/Sao_Paulo')
    
    @staticmethod
    def is_valid_date_format(date_str: str) -> bool:
        """Verifica se a string está no formato de data brasileiro dd/mm/yyyy"""
        if not date_str:
            return False
        
        pattern = r'^(\d{2}/\d{2}/\d{4})$'
        return bool(re.match(pattern, date_str))
    
    @staticmethod
    def is_valid_datetime_format(datetime_str: str) -> bool:
        """Verifica se a string está no formato de data e hora brasileiro dd/mm/yyyy HH:MM"""
        if not datetime_str:
            return False
        
        pattern = r'^(\d{2}/\d{2}/\d{4} \d{2}:\d{2})$'
        return bool(re.match(pattern, datetime_str))
    
    @classmethod
    def parse_brazilian_date(cls, date_str: str) -> Optional[datetime]:
        """
        Converte uma data no formato brasileiro (dd/mm/yyyy) para objeto datetime
        """
        if not cls.is_valid_date_format(date_str):
            return None
        
        try:
            # Converte string para datetime
            dt = datetime.strptime(date_str, '%d/%m/%Y')
            
            # Adiciona timezone de São Paulo
            return cls.TIMEZONE.localize(dt)
        except ValueError:
            return None
    
    @classmethod
    def parse_brazilian_datetime(cls, datetime_str: str) -> Optional[datetime]:
        """
        Converte uma data e hora no formato brasileiro (dd/mm/yyyy HH:MM) para objeto datetime
        """
        if not cls.is_valid_datetime_format(datetime_str):
            return None
        
        try:
            # Converte string para datetime
            dt = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')
            
            # Adiciona timezone de São Paulo
            return cls.TIMEZONE.localize(dt)
        except ValueError:
            return None
    
    @classmethod
    def to_brazilian_date(cls, dt: Union[datetime, str]) -> str:
        """
        Converte um objeto datetime ou string ISO para formato de data brasileira (dd/mm/yyyy)
        """
        if isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
            except ValueError:
                try:
                    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return ""
        
        # Se não tem timezone, assume que é UTC e converte para São Paulo
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
            
        # Converte para timezone de São Paulo
        local_dt = dt.astimezone(cls.TIMEZONE)
        
        # Retorna no formato brasileiro
        return local_dt.strftime('%d/%m/%Y')
    
    @classmethod
    def to_brazilian_datetime(cls, dt: Union[datetime, str]) -> str:
        """
        Converte um objeto datetime ou string ISO para formato de data e hora brasileira (dd/mm/yyyy HH:MM)
        """
        if isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
            except ValueError:
                try:
                    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return ""
        
        # Se não tem timezone, assume que é UTC e converte para São Paulo
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
            
        # Converte para timezone de São Paulo
        local_dt = dt.astimezone(cls.TIMEZONE)
        
        # Retorna no formato brasileiro
        return local_dt.strftime('%d/%m/%Y %H:%M')
    
    @classmethod
    def to_db_date(cls, date_str: str) -> Optional[str]:
        """
        Converte uma data no formato brasileiro (dd/mm/yyyy) para formato do banco de dados (yyyy-mm-dd)
        """
        dt = cls.parse_brazilian_date(date_str)
        if not dt:
            return None
        
        return dt.strftime('%Y-%m-%d')
    
    @classmethod
    def to_db_datetime(cls, datetime_str: str) -> Optional[str]:
        """
        Converte uma data e hora no formato brasileiro (dd/mm/yyyy HH:MM) para formato do banco de dados (yyyy-mm-dd HH:MM:SS)
        """
        dt = cls.parse_brazilian_datetime(datetime_str)
        if not dt:
            return None
        
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    @classmethod
    def now_brazilian_format(cls) -> str:
        """Retorna a data e hora atual no formato brasileiro"""
        now = datetime.now(cls.TIMEZONE)
        return cls.to_brazilian_datetime(now)
    
    @classmethod
    def now_db_format(cls) -> str:
        """Retorna a data e hora atual no formato do banco de dados"""
        now = datetime.now(cls.TIMEZONE)
        return now.strftime('%Y-%m-%d %H:%M:%S')
    
    @classmethod
    def process_form_data(cls, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa dados de formulário convertendo campos de data para o formato do banco de dados
        """
        processed_data = {}
        
        for key, value in form_data.items():
            if isinstance(value, str):
                # Se o campo parece ser uma data no formato brasileiro
                if key.startswith('data_') and cls.is_valid_date_format(value):
                    processed_data[key] = cls.to_db_date(value)
                
                # Se o campo parece ser uma data e hora no formato brasileiro
                elif ('_hora' in key or key == 'created_at' or key == 'updated_at') and cls.is_valid_datetime_format(value):
                    processed_data[key] = cls.to_db_datetime(value)
                
                # Para outros campos, mantenha o valor original
                else:
                    processed_data[key] = value
            else:
                processed_data[key] = value
        
        return processed_data
    
    @classmethod
    def format_model_to_response(cls, model_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formata os dados do modelo para resposta, convertendo datas para formato brasileiro
        """
        response = {}
        
        for key, value in model_dict.items():
            if value is None:
                response[key] = value
                continue
                
            # Trata campos de data
            if key.startswith('data_') and isinstance(value, (str, datetime)):
                response[key] = cls.to_brazilian_date(value)
            
            # Trata campos de data e hora
            elif ('_hora' in key or key == 'created_at' or key == 'updated_at') and isinstance(value, (str, datetime)):
                response[key] = cls.to_brazilian_datetime(value)
            
            # Para outros campos, mantenha o valor original
            else:
                response[key] = value
        
        return response