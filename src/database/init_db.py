from database.session import POSTGRES_ENGINE, MYSQL_ENGINE
from database.base import Base

def init_postgres():
    Base.metadata.create_all(bind=POSTGRES_ENGINE)

def init_mysql():
    Base.metadata.create_all(bind=MYSQL_ENGINE)
