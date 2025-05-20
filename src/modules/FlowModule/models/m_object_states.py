from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,func
from database.base import Base

class MObjectState(Base):
    __tablename__ = 'm_object_states'


    id = Column(Integer, primary_key=True)
    reference = Column(String, nullable=True)
    name = Column(String, nullable=True)
    active = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)