from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.app.modules.document_rules_module.models.document_rules import DocumentRule
from src.app.modules.entity_documents_module.models.entity_documents import EntityDocument
from src.app.modules.notifications_module.models.notifications import Notification
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Attribute(BaseModel):
    __tablename__ = "m_attributes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="Nombre del atributo")
    description = Column(String(200), nullable=True, comment="Descripción")
    parameter_id = Column(Integer, ForeignKey("m_parameters.id"), nullable=False, comment="Parámetro principal")
    reference = Column(String(200), nullable=True, comment="Referencia")
    state = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    parameters = relationship("Parameter", back_populates="attributes")

    # Relaciones inversas hacia DocumentRule
    document_type_rules = relationship(
        "DocumentRule",
        back_populates="document_types",
        foreign_keys=[DocumentRule.document_type_id]
    )

    stage_rules = relationship(
        "DocumentRule",
        back_populates="stages",
        foreign_keys=[DocumentRule.stage_id]
    )
    # ==============================================
    
    # Relaciones inversas hacia EntityDocument
    document_types_entity_documents = relationship(
        "EntityDocument",
        back_populates="document_types",
        foreign_keys=[EntityDocument.document_type_id]
    )


    stages_entity_documents = relationship(
        "EntityDocument",
        back_populates="stages",
        foreign_keys=[EntityDocument.stage_id]
    )
    
    document_status_entity_documents = relationship(
        "EntityDocument",
        back_populates="document_status",
        foreign_keys=[EntityDocument.document_status_id]
    )
    # ==============================================

    # Relaciones inversas hacia Notification
    notifications = relationship("Notification",back_populates="type_notification")