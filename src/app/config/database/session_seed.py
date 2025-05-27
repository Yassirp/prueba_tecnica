from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .db_connection import Connection
from contextlib import asynccontextmanager
from typing import AsyncGenerator


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .db_connection import Connection
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from dotenv import load_dotenv
import os

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.env'))
load_dotenv(dotenv_path)

DATABASE_URL = f'postgresql+asyncpg://{os.getenv("PG_USER")}:{os.getenv("PG_PASSWORD")}@{os.getenv("APP_HOST")}:{os.getenv("PORT_DOCKER")}/{os.getenv("PG_NAME")}'

# Crear el engine asíncrono
ENGINE_SEED = create_async_engine(
    DATABASE_URL, 
    echo=True,
    pool_size=10,  # Máximo de conexiones en el pool
    max_overflow=20,  # Conexiones adicionales si pool está lleno
    pool_timeout=30,  # Tiempo máximo (s) para esperar una conexión
    pool_recycle=1800,  # Recicla conexiones cada 30 min (evita idle)
)

# Crear sessionmaker asíncrono
SessionLocalSeed = async_sessionmaker(
    ENGINE_SEED,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# Dependencia para FastAPI con async
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocalSeed() as db:
        yield db


# Context manager si lo necesitas por fuera de FastAPI (por ejemplo en tareas)
@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocalSeed() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
