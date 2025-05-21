from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .db_connection import Connection
from contextlib import asynccontextmanager
from typing import AsyncGenerator

# Crear el engine asíncrono
ENGINE = create_async_engine(
    Connection.URL,
    echo=True,
    pool_size=10,             # Máximo de conexiones en el pool
    max_overflow=20,          # Conexiones adicionales si pool está lleno
    pool_timeout=30,          # Tiempo máximo (s) para esperar una conexión
    pool_recycle=1800,        # Recicla conexiones cada 30 min (evita idle)
)

# Crear sessionmaker asíncrono
PostgresSessionLocal = sessionmaker(
    bind=ENGINE,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Dependencia para FastAPI con async
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with PostgresSessionLocal() as db:
        yield db

# Context manager si lo necesitas por fuera de FastAPI (por ejemplo en tareas)
@asynccontextmanager
async def get_db_context():
    async with PostgresSessionLocal() as db:
        yield db
