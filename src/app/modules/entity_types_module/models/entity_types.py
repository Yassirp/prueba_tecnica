from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class EntityType(BaseModel):
    __tablename__ = "m_entity_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    state = Column(Integer, nullable=False, default=1)
    project_id = Column(Integer, ForeignKey("m_projects.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="entity_types")
    document_rule = relationship("DocumentRule", back_populates="entity_type")
