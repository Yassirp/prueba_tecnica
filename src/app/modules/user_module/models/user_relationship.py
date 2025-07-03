from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey,CheckConstraint
from src.app.shared.bases.base_model import BaseModel   
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz
from src.app.modules.flow_module.models.object_states import ObjectState
from src.app.modules.parameters_module.models.parameters_values import ParameterValue

class UserRelationship(BaseModel):
    __tablename__ = "c_user_relationship"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("m_users.id"), nullable=False, comment="ID del usuario.")
    user_relationship_id = Column(Integer, ForeignKey("m_users.id"), nullable=False, comment="ID del usuario con el que tiene la relación.")
    relationship_type_id = Column(Integer, ForeignKey("m_parameters_values.id"), nullable=False, comment="Tipo de relación entre usuarios. ")
    relationship_status_id = Column(Integer, ForeignKey("m_object_states.id"), nullable=False, comment="Estado de la relación entre usuarios.")
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    user = relationship("User", back_populates="user_relationships", foreign_keys=[user_id])
    #user_relationship = relationship("User", foreign_keys=[user_relationship_id])
    relationship_status = relationship("ObjectState", backref="user_relationships", foreign_keys=[relationship_status_id]) 
    relationship_type = relationship("ParameterValue", backref="user_relationships", foreign_keys=[relationship_type_id])
    
    __table_args__ = (
        CheckConstraint('user_id != user_relationship_id', name='check_user_ids_not_equal'),
    )