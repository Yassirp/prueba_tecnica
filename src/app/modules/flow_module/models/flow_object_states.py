from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz


class FlowObjectState(BaseModel):
    __tablename__ = 'm_flow_object_states'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    flow_id = Column(Integer, ForeignKey('m_flows.id'))
    object_state_id = Column(Integer, ForeignKey('m_object_states.id'))
    order_state = Column(Integer)
    role_assigned_id = Column(String, nullable=True)
    user_assigned_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
