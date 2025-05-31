from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from src.app.modules.attributes_module.models.attributes import Attribute
from sqlalchemy.orm import relationship
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Parameter(BaseModel):
    __tablename__ = "m_parameters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="Hace referencia al nombre del parametro.")
    description = Column(String(200), nullable=True, comment="Hace referencia a la descripcion del parametro.")
    state = Column(Integer, nullable=False, default=1, comment="Hace referencia a si el estado esta activo (1) o no(0).")
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    attributes = relationship("Attribute", back_populates="parameters")




