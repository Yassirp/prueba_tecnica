from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey,func
from database.base import Base
from sqlalchemy.orm import relationship
class CModuleAction(Base):
    __tablename__ = 'c_modules_actions'

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey('m_modules.id'))
    action_id = Column(Integer, ForeignKey('m_actions.id'))
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    permissions = relationship("CPermission", back_populates="module_action")
    module = relationship("MModule", back_populates="module_actions")
    action = relationship("MAction", back_populates="module_actions")