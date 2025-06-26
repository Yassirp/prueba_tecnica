from sqlalchemy import Column, Integer, Text, DateTime, String, Boolean, TIMESTAMP,func, ForeignKey
from src.app.shared.bases.base_model import BaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

class Action(BaseModel):
    __tablename__ = 'm_actions'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    type_id = Column(Integer, ForeignKey('m_parameters_values.id'), nullable=True)
    name = Column(String)
    active = Column(Boolean)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    module_actions = relationship("ModuleAction", back_populates="action")