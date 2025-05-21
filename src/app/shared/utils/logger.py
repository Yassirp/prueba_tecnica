import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def setup_logger(name: str = None) -> logging.Logger:
    """
    Configura y retorna un logger con formato personalizado y handlers para consola y archivo.
    
    Args:
        name (str, optional): Nombre del logger. Si es None, usa el nombre del módulo.
    
    Returns:
        logging.Logger: Logger configurado
    """
    # Crear el logger
    logger = logging.getLogger(name or __name__)
    logger.setLevel(logging.INFO)

    # Evitar duplicación de handlers
    if logger.handlers:
        return logger

    # Crear directorio de logs si no existe
    log_dir = os.path.join("src", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Formato del log
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # Handler para archivo
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, f'app_{current_date}.log'),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger

def log_error(logger: logging.Logger, error: Exception, context: str = None):
    """
    Registra un error con contexto adicional.
    
    Args:
        logger (logging.Logger): Logger a utilizar
        error (Exception): Error a registrar
        context (str, optional): Contexto adicional del error
    """
    error_msg = f"{context + ': ' if context else ''}{str(error)}"
    logger.error(error_msg, exc_info=True)

def log_info(logger: logging.Logger, message: str, **kwargs):
    """
    Registra un mensaje informativo con datos adicionales.
    
    Args:
        logger (logging.Logger): Logger a utilizar
        message (str): Mensaje a registrar
        **kwargs: Datos adicionales a incluir en el mensaje
    """
    if kwargs:
        message = f"{message} - {kwargs}"
    logger.info(message)

def log_warning(logger: logging.Logger, message: str, **kwargs):
    """
    Registra un mensaje de advertencia con datos adicionales.
    
    Args:
        logger (logging.Logger): Logger a utilizar
        message (str): Mensaje a registrar
        **kwargs: Datos adicionales a incluir en el mensaje
    """
    if kwargs:
        message = f"{message} - {kwargs}"
    logger.warning(message)

def log_debug(logger: logging.Logger, message: str, **kwargs):
    """
    Registra un mensaje de depuración con datos adicionales.
    
    Args:
        logger (logging.Logger): Logger a utilizar
        message (str): Mensaje a registrar
        **kwargs: Datos adicionales a incluir en el mensaje
    """
    if kwargs:
        message = f"{message} - {kwargs}"
    logger.debug(message) 