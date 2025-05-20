from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from sqlalchemy.sql import func
from database.base import Base

class Contract(Base):
    __tablename__ = 'contratos'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_director = Column(BigInteger, nullable=True)
    name = Column(String(255), nullable=True)
    code = Column(String(255), nullable=True)
    id_gerente = Column(String(255), nullable=True)
    data = Column(String(255), nullable=True)
    user_create = Column(String(255), nullable=True)
    resolution_number = Column(String(255), nullable=True)
    document_date = Column(String(255), nullable=True)
    esquema = Column(String(255), nullable=True)
    valor = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)

