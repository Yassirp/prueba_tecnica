from sqlalchemy import Column, Integer, Text, DateTime, String, Boolean, TIMESTAMP,func, ForeignKey
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Action(BaseModel):
    __tablename__ = 'm_actions'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    type_id = Column(Integer, ForeignKey('m_parameters_values.id'), nullable=True)
    name = Column(String)
    active = Column(Boolean)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
