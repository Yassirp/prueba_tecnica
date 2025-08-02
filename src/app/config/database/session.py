from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .db_connection import Connection
from contextlib import contextmanager
from typing import Generator

# Crear el engine síncrono
ENGINE = create_engine(
    Connection.URL,
    echo=True,
    pool_size=10,  # Máximo de conexiones en el pool
    max_overflow=20,  # Conexiones adicionales si pool está lleno
    pool_timeout=30,  # Tiempo máximo (s) para esperar una conexión
    pool_recycle=1800,  # Recicla conexiones cada 30 min (evita idle)
)

# Crear sessionmaker síncrono
SessionLocal = sessionmaker(
    bind=ENGINE,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# Dependencia para FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Context manager si lo necesitas por fuera de FastAPI (por ejemplo en tareas)
@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
