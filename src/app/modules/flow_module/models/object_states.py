from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class ObjectState(BaseModel):
    __tablename__ = 'm_object_states'


    id = Column(Integer, primary_key=True)
    reference = Column(String, nullable=True)
    name = Column(String, nullable=True)
    active = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)