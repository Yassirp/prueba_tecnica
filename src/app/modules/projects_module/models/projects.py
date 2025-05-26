from sqlalchemy import Column, Integer, String, DateTime, func
from src.app.shared.bases.base_model import BaseModel
from sqlalchemy.orm import relationship

class Project(BaseModel):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    state = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    entity_types = relationship("EntityType", back_populates="project")
