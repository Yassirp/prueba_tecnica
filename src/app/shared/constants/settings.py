import os

class Settings: 
    """ Environmental variables """

    HOST = os.getenv("HOST_IP")
    PORT = os.getenv("HOST_PORT") 
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    DB_NAME = os.getenv("PG_NAME")
    DB_HOST = os.getenv("PG_HOST") 
    DB_PORT = os.getenv("PG_PORT")   
    DB_USERNAME = os.getenv("PG_USER")
    DB_PASSWORD = os.getenv("PG_PASSWORD")

    SECRET_KEY=os.getenv("SECRET_KEY")
    APP_KEY=os.getenv("APP_KEY", "")
    ALLOWED_ORIGINS=os.getenv("ALLOWED_ORIGINS", "")

    APP_NAME="Micro Documents API"
    APP_DESCRIPTION="API for document management"
    APP_VERSION="1.0.0"
