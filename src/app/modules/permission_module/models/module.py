from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Module(BaseModel):
    __tablename__ = 'm_modules'

    id = Column(Integer, primary_key=True)
    level = Column(Integer)
    name = Column(String)
    path = Column(String)
    parent_id = Column(Integer)
    active = Column(Boolean)
    position = Column(Integer)
    icon = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
