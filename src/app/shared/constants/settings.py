import os

class Settings:
    """Environmental variables"""

    HOST = os.getenv("HOST_IP")
    PORT = os.getenv("HOST_PORT")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    DB_NAME = os.getenv("PG_NAME")
    DB_HOST = os.getenv("PG_HOST")
    DB_PORT = os.getenv("PG_PORT")
    DB_USERNAME = os.getenv("PG_USER")
    DB_PASSWORD = os.getenv("PG_PASSWORD")

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
    
    APP_NAME = "Micro LVR API"
    APP_DESCRIPTION = "API for LVR management"
    APP_VERSION = "0.0.1"

