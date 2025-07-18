# Archivo generado automáticamente para sedes - models
from sqlalchemy import Column, Integer, Text, DateTime, String, Boolean, TIMESTAMP,func, ForeignKey
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship
import pytz

class Sede(BaseModel):
    __tablename__ = 'm_sedes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    type_id = Column(Integer, ForeignKey('m_parameters_values.id'), nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    description = Column(String, nullable=True)
    active = Column(Boolean)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

