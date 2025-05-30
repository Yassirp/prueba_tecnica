from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Attribute(BaseModel):
    __tablename__ = "m_attributes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="Hace referecnia al nombre del atributo.")
    description = Column(String(200), nullable=True, comment="Hace referencia la descripcion.")
    parameter_id = Column(Integer, ForeignKey("m_parameters.id"), nullable=False, comment="Hace referencia parámetro principal (id de parameters).")
    reference  = Column(String(200), nullable=True, comment="Hace referencia a la descripcion del parametro.")
    state = Column(Integer, nullable=False, default=1, comment="Hace referencia a si el estado esta activo (1) o no(0).")
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    #Relaciones a con otros modelos 
    parameter = relationship("Parameter", back_populates="attributes")
    document_types = relationship("DocumentRule", back_populates="document_types", foreign_keys="[DocumentRule.document_type_id]")
    stages = relationship("DocumentRule", back_populates="stages", foreign_keys="[DocumentRule.stage_id]")
