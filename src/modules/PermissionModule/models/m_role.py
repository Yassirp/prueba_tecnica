from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,func
from database.base import Base
from sqlalchemy.orm import relationship
class MRole(Base):
    __tablename__ = 'm_roles'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    old_id = Column(Integer)
    active = Column(Boolean)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)


    permissions = relationship("CPermission", back_populates="role")