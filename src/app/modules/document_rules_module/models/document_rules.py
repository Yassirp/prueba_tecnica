from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class DocumentRule(BaseModel):
    __tablename__ = "m_document_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="Hace referencia al nombre del parámetro.")
    project_id = Column(Integer, ForeignKey("m_projects.id"), nullable=False)
    document_type_id = Column(Integer, ForeignKey("m_attributes.id"), nullable=False, comment="Tipo de documento")
    entity_type_id = Column(Integer, ForeignKey("m_entity_types.id"), nullable=False, comment="Tipo de entidad")
    stage_id = Column(Integer, ForeignKey("m_attributes.id"), nullable=False, comment="Etapa")
    description = Column(String(200), nullable=True, comment="Descripción")
    allowed_file_type = Column(JSON, nullable=True, comment="Tipo de archivo permitido")
    is_required = Column(Boolean, default=False, nullable=False)
    max_file_size  = Column(Integer, nullable=True, comment="Tamaño máximo del archivo")
    state = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    project = relationship("Project", back_populates="document_rule")
    entity_types = relationship("EntityType", back_populates="document_rules")
    document_types = relationship("Attribute", back_populates="document_type_rules", foreign_keys=[document_type_id])
    stages = relationship("Attribute", back_populates="stage_rules", foreign_keys=[stage_id])
