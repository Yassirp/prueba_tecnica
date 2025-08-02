import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    """Environmental variables"""

    APP_ENV = os.getenv("APP_ENV", "testing")
    HOST = os.getenv("HOST_IP")
    PORT = os.getenv("HOST_PORT")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USERNAME = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    APP_KEY = os.getenv("APP_KEY", "")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "")
    
    MAIL_HOST = os.getenv("MAIL_HOST", "")
    MAIL_PORT = os.getenv("MAIL_PORT", 587)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM_ADDRESS = os.getenv("MAIL_FROM_ADDRESS", "")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "")
    MAIL_ENCRYPTION = os.getenv("MAIL_ENCRYPTION", "tls")
    
    CELL_URL = os.getenv("CELL_URL", "")
    CELL_USERNAME = os.getenv("CELL_USERNAME", "")
    CELL_PASSWORD = os.getenv("CELL_PASSWORD", "")
    CELL_CODE = os.getenv("CELL_CODE", "")
    
    APP_NAME = "Prueba Naowee"
    APP_DESCRIPTION = "API para gestión de reservas de canchas de fútbol"
    APP_VERSION = "0.0.1"

    AWS_ACCESS_KEY_ID= os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY= os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION= os.getenv("AWS_REGION", "")
    S3_BUCKET= os.getenv("S3_BUCKET_NAME", "")
    MERCADO_PAGO_TOKEN = os.getenv("MERCADO_PAGO_TOKEN", "test_token")
    MERCADO_PAGO_WEBHOOK_PASSWORD = os.getenv("MERCADO_PAGO_WEBHOOK_PASSWORD", "test_password")