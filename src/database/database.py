from contextlib import contextmanager
from .session import PostgresSessionLocal, MySQLSessionLocal

@contextmanager
def get_db():
    db = PostgresSessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_mysql():
    db = MySQLSessionLocal()
    try:
        yield db
    finally:
        db.close()
