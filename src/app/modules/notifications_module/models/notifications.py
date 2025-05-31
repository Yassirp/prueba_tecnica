# Archivo generado autom�ticamente para notifications - models
from src.app.shared.bases.base_model import BaseModel
from sqlalchemy import (
    Column, Integer, String, 
    DateTime, ForeignKey, JSON, 
    Text, Boolean
    )
from datetime import datetime
from sqlalchemy.orm import relationship
import pytz

class Notification(BaseModel):
    __tablename__ = "o_notifications"

    id = Column(Integer, primary_key=True, index=True)
    #entity_document_id = Column(Integer, ForeignKey("m_entity_documents.id"), nullable=False)
    type_notification_id = Column(Integer, ForeignKey("m_attributes.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)
    link = Column(Text, nullable=True)
    is_read = Column(Boolean, nullable=False, default=False)
    state = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones a otros modelos
    #entity_document = relationship("EntityDocument", back_populates="notifications")
    type_notification = relationship("Attribute", back_populates="notifications")
