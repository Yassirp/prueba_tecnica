from sqlalchemy import Column, Integer, Text, DateTime, String
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
    password = Column(String, nullable=False)
    phone = Column(Text, nullable=True, comment="Teléfono del usuario.")
    address = Column(Text, nullable=True, comment="Dirección del usuario.")
    city_id = Column(Integer, nullable=True, comment="Ciudad del usuario.")
    country_id = Column(Integer, nullable=False, comment="País del usuario.")
    zip_code = Column(Text, nullable=True, comment="Código postal del usuario.")
    role_id = Column(Integer, nullable=False, comment="Rol del usuario.")
    created_by = Column(Integer, nullable=True, comment="Usuario que creó el usuario.")
    state = Column(Integer, nullable=True, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)