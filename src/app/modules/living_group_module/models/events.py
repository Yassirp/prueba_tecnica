from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, DECIMAL
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Event(BaseModel):
    __tablename__ = 'o_events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    living_group_id = Column(Integer, ForeignKey('o_living_groups.id'), nullable=True)
    max_members = Column(Integer, nullable=True, default=0)
    min_members = Column(Integer, nullable=True, default=0)
    out = Column(Boolean, default=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)