from sqlalchemy import Column, Integer, Text, DateTime, String, ForeignKey, JSON,and_, Boolean
from src.app.shared.bases.base_model import BaseModel   
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
import pytz
from src.app.modules.document_module.models.documents import Document
from src.app.modules.ubication_module.models.countries import Country
from src.app.modules.ubication_module.models.departments import Department
from src.app.modules.ubication_module.models.municipalities import Municipality
from src.app.modules.permission_module.models.role import Role
from sqlalchemy import Computed
from src.app.modules.user_module.models.user_relationship import UserRelationship

class User(BaseModel):
    __tablename__ = "m_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    search_text = Column(Text, Computed("lower(name || ' ' || last_name || ' ' || email || ' ' || document_number)"), nullable=True)
    name = Column(Text, nullable=False, comment="Nombre del usuario.")
    last_name = Column(Text, nullable=False, comment="Apellido del usuario.")
    document_type = Column(Integer, ForeignKey("m_parameters_values.id"), nullable=True, comment="Tipo de documento del usuario.")
    document_number = Column(Text, nullable=False, comment="Número de documento del usuario.")
    email = Column(Text, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(Text, nullable=True, comment="Teléfono del usuario.")
    address = Column(Text, nullable=True, comment="Dirección del usuario.")
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False, comment="País del usuario.")
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, comment="Departamento del usuario.")
    municipality_id = Column(Integer, ForeignKey("municipalities.id"), nullable=False, comment="Municipio del usuario.")
    zip_code = Column(Text, nullable=True, comment="Código postal del usuario.")
    role_id = Column(Integer, ForeignKey("m_roles.id"), comment="Rol del usuario.")
    created_by = Column(Integer, ForeignKey("m_users.id"), nullable=True, comment="Usuario que creó el usuario.")
    state = Column(Integer, nullable=True, default=1)
    code = Column(String, nullable=True, comment="Código del usuario.")
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    
    campus = Column(Integer, ForeignKey("m_sedes.id"), nullable=True, comment="Campus al que pertenece el usuario.")
    time = Column(String, nullable=True, comment="Tiempo que lleva en LivingRoom.")
    courses = Column(Text, nullable=True, comment="Cursos realizados por el usuario (lista separada por comas).")
    participated_in_living_group = Column(Integer, nullable=True, comment="1 si sí, 0 si no.")
    #living_group_name = Column(String, nullable=True, comment="Nombre del grupo (si aplica).")
    did_camp = Column(Integer, nullable=True, comment="1 si sí, 0 si no.")
    
    
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    data = Column(JSON, nullable=True, comment="Datos complementarios del usuario.")
    
    country = relationship("Country", backref="users", foreign_keys=[country_id])
    department = relationship("Department", backref="users", foreign_keys=[department_id])
    municipality = relationship("Municipality", backref="users", foreign_keys=[municipality_id])
    role = relationship("Role", backref="users", foreign_keys=[role_id])
    document_type_relationship = relationship("ParameterValue", backref="users", foreign_keys=[document_type])
    created_by_user = relationship("User", remote_side="User.id", backref="created_users")
    getLivingGroupUsers = relationship("LivingGroupUser", back_populates="getUser")
    associated_documents = relationship(
        "Document",
        primaryjoin=lambda: and_(
            foreign(Document.associate_id) == User.id,
            Document.associate_to == 'users'
        ),
        viewonly=True,
        lazy="selectin"
    )
    
    user_relationships = relationship(
        "UserRelationship",
        foreign_keys="[UserRelationship.user_id]",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    getSede = relationship("Sede", backref="getUsers")