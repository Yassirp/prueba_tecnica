from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey,func
from database.base import Base
from sqlalchemy.orm import relationship

class MAction(Base):
    __tablename__ = 'm_actions'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    type_id = Column(Integer, ForeignKey('m_parameters_values.id'), nullable=True)
    name = Column(String)
    active = Column(Boolean)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    module_actions = relationship("CModuleAction", back_populates="action")