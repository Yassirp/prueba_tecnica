# Archivo generado automáticamente para entity_documents - models
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.app.modules.entity_document_logs_module.models.entity_document_logs import EntityDocumentLog
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class EntityDocument(BaseModel):
    __tablename__ = "m_entity_documents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("m_projects.id"), comment="Hace referencia al id del proyecto.", nullable=False)
    document_type_id = Column(Integer, ForeignKey("m_attributes.id"), comment="Hace refenrecia al id del tipo de documento.", nullable=False)
    entity_type_id = Column(Integer, ForeignKey("m_entity_types.id"), comment="Hace referencia la tipo de entidad.", nullable=False)
    entity_id = Column(Integer, nullable=True, comment="Hace referencia al id de la entidad externa (estudiante o deportista).")
    stage_id = Column(Integer, ForeignKey("m_attributes.id"), nullable=False, comment="Hace referencia a la Etapa.")
    file_url = Column(String(1000), nullable=True, comment="Hace referencia a la ruta de S3.")
    file_extension  = Column(String(100), nullable=True, comment="Hace referencia a la extension.")
    file_size = Column(Integer, nullable=True, comment="Hace referencia al tamaño del archivo.")
    mime_type = Column(Integer, nullable=True, comment="Hace referencia al tipo minimo.")
    upload_device = Column(String(100), nullable=True, comment="Subir a dispositivo.")
    upload_ip = Column(String(100), nullable=True, comment="Ip del dispositivo.")
    document_status_id =  Column(Integer, ForeignKey("m_attributes.id"), comment="Hace refenrecia al estado del documento.", nullable=False)
    observations = Column(String(100), nullable=True, comment="Hace referencia a la observacion.")
    state = Column(Integer, nullable=False, default=1)
    created_by = Column(Integer, nullable=True, comment="Hace referencia al usario de creacion.")
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    project = relationship("Project", back_populates="entity_documents")
    entity_types = relationship("EntityType", back_populates="entity_documents")
    document_types = relationship("Attribute", back_populates="document_types_entity_documents",foreign_keys=[document_type_id])
    stages = relationship("Attribute", back_populates="stages_entity_documents",foreign_keys=[stage_id])
    document_status = relationship("Attribute", back_populates="document_status_entity_documents", foreign_keys=[document_status_id])
    notifications = relationship("Notification", back_populates="entity_document")

    # Relaciones inversas hacia EntityDocumentLog
    entity_document_logs = relationship(
        "EntityDocumentLog",
        back_populates="entity_document",
        foreign_keys=[EntityDocumentLog.entity_document_id]
    )

