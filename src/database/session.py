from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_connection import Connection

# PostgreSQL
POSTGRES_ENGINE = create_engine(Connection.URL)
PostgresSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=POSTGRES_ENGINE)

# MySQL
MYSQL_ENGINE = create_engine(Connection.MYSQL_URL)
MySQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=MYSQL_ENGINE)
