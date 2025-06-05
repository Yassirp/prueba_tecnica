# Archivo generado autom�ticamente para entity_document_logs - models
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, BigInteger
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship
import pytz

class EntityDocumentLog(BaseModel):
    __tablename__ = "m_entity_document_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity_document_id = Column(Integer, ForeignKey("m_entity_documents.id"), nullable=False)
    action = Column(String(200), nullable=False)
    observations = Column(Text(), nullable=True)
    before = Column(JSON, nullable=True)
    after = Column(JSON, nullable=True)
    created_by = Column(BigInteger, nullable=False)
    state = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relaciones a otros modelos
    entity_document = relationship("EntityDocument", back_populates="entity_document_logs", foreign_keys=[entity_document_id])


