from sqlalchemy import Column, Integer, DateTime, ForeignKey
from src.app.shared.bases.base_model import BaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

class ModuleAction(BaseModel):
    __tablename__ = 'c_modules_actions'

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey('m_modules.id'))
    action_id = Column(Integer, ForeignKey('m_actions.id'))
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
