# Archivo generado automáticamente para living_group - models
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, DECIMAL
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz
from sqlalchemy.orm import relationship

class LivingGroup(BaseModel):
    __tablename__ = 'o_living_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)
    max_members = Column(Integer, nullable=True, default=0)
    min_members = Column(Integer, nullable=True, default=0)
    value = Column(DECIMAL(10, 2), nullable=True, default=0)
    sede_id = Column(Integer, ForeignKey('m_sedes.id'), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    getSede = relationship("Sede", foreign_keys=[sede_id], back_populates="getLivingGroups")