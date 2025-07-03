from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,func
from src.app.shared.bases.base_model import BaseModel
from sqlalchemy.orm import relationship

class Role(BaseModel):
    __tablename__ = 'm_roles'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    active = Column(Boolean)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    permissions = relationship("Permission", back_populates="role", cascade="all, delete-orphan")