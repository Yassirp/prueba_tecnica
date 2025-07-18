from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, JSON
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class LivingGroupUser(BaseModel):
    __tablename__ = 'o_living_group_users'

    id = Column(Integer, primary_key=True)
    living_group_id = Column(Integer, ForeignKey('o_living_groups.id'))
    user_id = Column(Integer, ForeignKey('m_users.id'))
    type_id = Column(Integer, ForeignKey('m_parameters_values.id'), nullable=True)
    description = Column(String, nullable=True)
    data = Column(JSON, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)