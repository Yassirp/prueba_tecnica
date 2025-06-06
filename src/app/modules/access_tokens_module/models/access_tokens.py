# Archivo generado automáticamente para access_tokens - models
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from src.app.shared.bases.base_model import BaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

class AccessToken(BaseModel):
    __tablename__ = "m_access_tokens"

    token = Column(Text, primary_key=True, nullable=False)
    project_id = Column(Integer, ForeignKey("m_projects.id"), comment="Hace referencia al id del proyecto.", nullable=False)
    user_id  = Column(Integer, nullable=True, comment="Hace referencia al id del usuario en sistema.")
    state = Column(Integer, nullable=False, default=1)
    expires_at = Column(DateTime(timezone=True), nullable=True, comment="Tiempo de expiracion del token.")
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones    
    project = relationship("Project", back_populates="access_tokens")