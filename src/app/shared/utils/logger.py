import logging
from typing import Optional, Any


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    logger = logging.getLogger(name)

    if level is not None:
        logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_error(
    logger: logging.Logger, error: Exception, context: Optional[str] = None
) -> None:
    """
    Registra un error con contexto adicional.

    Args:
        logger (logging.Logger): Logger a utilizar
        error (Exception): Error a registrar
        context (str, optional): Contexto adicional del error
    """
    error_msg = f"{context + ': ' if context else ''}{str(error)}"
    logger.error(error_msg, exc_info=True)


def log_info(logger: logging.Logger, message: str, **kwargs: Any) -> None:
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


def log_warning(logger: logging.Logger, message: str, **kwargs: Any) -> None:
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


def log_debug(logger: logging.Logger, message: str, **kwargs: Any) -> None:
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
