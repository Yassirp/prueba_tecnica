from sqlalchemy import Column, Integer, String, TIMESTAMP,ForeignKey,func
from database.base import Base

class MFlowObjectState(Base):
    __tablename__ = 'm_flow_object_states'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    flow_id = Column(Integer, ForeignKey('m_flows.id'))
    object_state_id = Column(Integer, ForeignKey('m_object_states.id'))
    order_state = Column(Integer)
    role_assigned_id = Column(String, nullable=True)
    user_assigned_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
