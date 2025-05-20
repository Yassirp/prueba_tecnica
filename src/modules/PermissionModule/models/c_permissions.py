from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey,func
from database.base import Base
from sqlalchemy.orm import relationship
class CPermission(Base):
    __tablename__ = 'c_permissions'

    id = Column(Integer, primary_key=True)
    associate_to = Column(String)
    associate_id = Column(Integer, ForeignKey('m_roles.id'))
    action_id = Column(Integer, ForeignKey('c_modules_actions.id'))
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    
    role = relationship("MRole", back_populates="permissions")
    module_action = relationship("CModuleAction", back_populates="permissions")