import os

class Settings: 
    """ Environmental variables """

    DB_HOST = os.getenv("PG_HOST") 
    DB_PORT = os.getenv("PG_PORT")   
    DB_NAME = os.getenv("PG_NAME")
    DB_USERNAME = os.getenv("PG_USER")
    DB_PASSWORD = os.getenv("PG_PASSWORD")
    HOST = os.getenv("HOST_IP")
    PORT = os.getenv("HOST_PORT") 
    HOST_PORT_SOCKET = os.getenv("HOST_PORT_SOCKET") 
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    REDIS_HOST=os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT=os.getenv("REDIS_PORT", 6379)
    REDIS_DECODE_RESPONSES=os.getenv("REDIS_DECODE_RESPONSES", True)
    REDIS_USERNAME=os.getenv("REDIS_USERNAME", "default")
    REDIS_PASSWORD=os.getenv("REDIS_PASSWORD", None)
    APP_KEY=os.getenv("APP_KEY", "")
    SECRET_KEY=os.getenv("SECRET_KEY")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_DB = os.getenv("MYSQL_DB")