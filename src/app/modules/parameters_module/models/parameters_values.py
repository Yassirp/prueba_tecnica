from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz
from ..models.parameters import Parameter

class ParameterValue(BaseModel):
    __tablename__ = 'm_parameters_values'

    id = Column(Integer, primary_key=True)
    parameter_id = Column(Integer, ForeignKey('m_parameters.id'))
    reference = Column(String)
    value = Column(String)
    description = Column(String)
    parent_id = Column(Integer, ForeignKey('m_parameters_values.id'))
    state = Column(Integer, nullable=False, default=1, comment="Hace referencia a si el estado esta activo (1) o no(0).")
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    getParameter = relationship("Parameter", back_populates="values", foreign_keys=[parameter_id])
    getParent = relationship("ParameterValue", remote_side=[id], back_populates="children", foreign_keys=[parent_id])
    children = relationship("ParameterValue", back_populates="getParent", foreign_keys=[parent_id])