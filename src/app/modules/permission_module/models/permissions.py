from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Permission(BaseModel):
    __tablename__ = 'c_permissions'

    id = Column(Integer, primary_key=True)
    associate_to = Column(String)
    associate_id = Column(Integer)
    module_action_id = Column(Integer, ForeignKey('c_modules_actions.id'))
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
