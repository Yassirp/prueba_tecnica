from sqlalchemy import Column, Integer, String, DateTime, func
from src.app.shared.bases.base_model import BaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

class Project(BaseModel):
    __tablename__ = "m_projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    state = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones    
    entity_types = relationship("EntityType", back_populates="project")
    document_rule = relationship("DocumentRule", back_populates="project")
    entity_documents = relationship("EntityDocument", back_populates="project")
