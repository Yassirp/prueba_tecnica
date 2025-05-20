from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey,func
from database.base import Base
from sqlalchemy.orm import relationship


class MParameterValue(Base):
    __tablename__ = 'm_parameters_values'

    id = Column(Integer, primary_key=True)
    parameter_id = Column(Integer, ForeignKey('m_parameters.id'))
    reference = Column(String)
    value = Column(String)
    description = Column(String)
    parent_id = Column(Integer, ForeignKey('m_parameters_values.id'))
    active = Column(Boolean)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
    
    getParameter = relationship("MParameter", back_populates="values", foreign_keys=[parameter_id])
    getParent = relationship("MParameterValue", remote_side=[id], back_populates="children", foreign_keys=[parent_id])
    children = relationship("MParameterValue", back_populates="getParent", foreign_keys=[parent_id])
    parent_product = relationship("MProduct", back_populates="unit_value")