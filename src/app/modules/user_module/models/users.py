from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, JSON
from src.app.shared.bases.base_model import BaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

class User(BaseModel):
    __tablename__ = "m_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, comment="Nombre del usuario.")
    last_name = Column(Text, nullable=False, comment="Apellido del usuario.")
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    phone = Column(Text, nullable=False, comment="Teléfono del usuario.")
    address = Column(Text, nullable=False, comment="Dirección del usuario.")
    city = Column(Text, nullable=False, comment="Ciudad del usuario.")
    country = Column(Text, nullable=False, comment="País del usuario.")
    zip_code = Column(Text, nullable=False, comment="Código postal del usuario.")
    role = Column(Text, nullable=False, comment="Rol del usuario.")
    status = Column(Text, nullable=False, comment="Estado del usuario.")
    created_by = Column(Integer, nullable=False, comment="Usuario que creó el usuario.")
    state = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)