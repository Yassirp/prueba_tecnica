from app.shared.bases.base_model import Base
from sqlalchemy import (
    Column, BigInteger, TinyInteger, String, DateTime
)
from datetime import datetime


class Project(Base):
    __tablename__ = "m_projects"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=True)
    state = Column(TinyInteger, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
