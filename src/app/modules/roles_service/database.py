import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Buscar el archivo .env en la carpeta src del proyecto
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env"))
load_dotenv(ENV_PATH)

# Tomar la variable de conexión específica del servicio
DATABASE_URL = os.getenv("DB_CUATRO")  # En canchas sería DB_CANCHAS, en reservas DB_RESERVAS, etc.

if not DATABASE_URL:
    raise ValueError(f"❌ No se encontró la variable DB_CUATRO en el archivo .env (Ruta: {ENV_PATH})")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
