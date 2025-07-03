from sqlalchemy import Column, Integer, Text, DateTime, String, ForeignKey, JSON,and_
from src.app.shared.bases.base_model import BaseModel   
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
import pytz


class UserRelationship(BaseModel):
    __tablename__ = "c_user_relationship"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("m_users.id"), nullable=False, comment="ID del usuario.")
    user_relationship_id = Column(Integer, ForeignKey("m_users.id"), nullable=False, comment="ID del usuario con el que tiene la relación.")
    relationship_type = Column(Text, nullable=False, comment="Tipo de relación entre usuarios.")
    relationship_status = Column(Integer, nullable=False, comment="Estado de la relación entre usuarios.")
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    user = relationship("User", backref="user_relationships", foreign_keys=[user_id])
    user_relationship = relationship("User", backref="user_relationships", foreign_keys=[user_relationship_id])