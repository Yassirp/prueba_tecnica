from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Role(BaseModel):
    __tablename__ = 'm_roles'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    active = Column(Boolean)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)