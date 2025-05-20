from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from sqlalchemy.sql import func
from database.base import Base

class ContratoAssignment(Base):
    __tablename__ = 'contratos_assigment'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_contrato = Column(String(255), nullable=True)
    associate_to = Column(String(255), nullable=True)
    associate_id = Column(String(255), nullable=True)
    schema = Column(String(255), nullable=True)
    parent_id = Column(String(255), nullable=True)
    cupos = Column(String(255), nullable=True)
    lostCupos = Column(String(100), nullable=True)
    data = Column(String(255), nullable=True)
    user_create = Column(String(255), nullable=True)
    valor = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)

    # contract=
