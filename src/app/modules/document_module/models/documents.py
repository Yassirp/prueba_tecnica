from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, JSON, ForeignKey
from sqlalchemy.orm import relationship
from src.app.shared.bases.base_model import BaseModel


class Document(BaseModel):
    __tablename__ = 'm_documents'

    id = Column(Integer, primary_key=True)
    associate_id = Column(Integer, nullable=True)
    associate_to = Column(String, nullable=True)

    document_type = Column(Integer, ForeignKey("m_parameters_values.id"), nullable=True)
    path = Column(String, nullable=True)
    url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    data = Column(JSON, nullable=True)

    created_by = Column(Integer, ForeignKey("m_users.id"), nullable=True)
    active = Column(Boolean, nullable=True, default=True)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    # Relaciones
    type = relationship("ParameterValue", backref="documents", foreign_keys=[document_type])
    user = relationship("User", backref="documents", foreign_keys=[created_by])
