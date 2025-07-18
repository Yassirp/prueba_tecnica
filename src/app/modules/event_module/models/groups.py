from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, DECIMAL
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Group(BaseModel):
    __tablename__ = 'm_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    max_members = Column(Integer, nullable=True, default=0)
    min_members = Column(Integer, nullable=True, default=0)
    value = Column(DECIMAL(10, 2), nullable=True, default=0)
    sede_id = Column(Integer, ForeignKey('m_sedes.id'), nullable=True)
    active = Column(Boolean)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)