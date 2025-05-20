from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,func
from database.base import Base
from sqlalchemy.orm import relationship

class MParameter(Base):
    __tablename__ = 'm_parameters'

    id = Column(Integer, primary_key=True)
    reference = Column(String)
    value = Column(String)
    active = Column(Boolean)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    values = relationship("MParameterValue", back_populates="getParameter", foreign_keys="MParameterValue.parameter_id")
