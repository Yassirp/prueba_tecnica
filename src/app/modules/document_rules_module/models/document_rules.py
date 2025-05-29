from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class DocumentRule(BaseModel):
    __tablename__ = "m_document_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="Hace referencia al nombre del parametro.")
    project_id = Column(Integer, ForeignKey("m_projects.id"), nullable=False)
    document_type_id = Column(Integer, ForeignKey("m_attributes.id"),comment="Hace referencia al tipo de documento.", nullable=False)
    entity_type_id = Column(Integer, ForeignKey("m_entity_types.id"),comment="Hace referencia al tipo de entidad.", nullable=False)
    stage_id = Column(Integer, ForeignKey("m_attributes.id"),comment="Hace referencia a la etapa.", nullable=False)
    description = Column(String(200), nullable=True, comment="Hace referencia a la descripcion del parametro.")
    allowed_file_type = Column(JSON, comment="Hace referencia al tipo de archivo.",nullable=True)
    is_required = Column(Boolean, default=False, nullable=False)
    max_file_size  = Column(Integer, comment="Tamaño del archivo a cargar.", nullable=True)
    state = Column(Integer, nullable=False, default=1, comment="Hace referencia a si el estado esta activo (1) o no(0).")
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    

    # Relaciones con otros modelos
    project = relationship("Project", back_populates="document_rule")
    document_type = relationship("Attribute", foreign_keys=[document_type_id], back_populates="document_type")
    stage = relationship("Attribute", foreign_keys=[stage_id], back_populates="stage")
    entity_type = relationship("EntityType", back_populates="document_rule")
