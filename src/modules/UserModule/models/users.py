from database.base import Base
from sqlalchemy import (
    Column, BigInteger, Integer, String, Text, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    role_id = Column(BigInteger, ForeignKey("roles.id"), nullable=False)
    document_type = Column(BigInteger, nullable=False)
    parent_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)

    name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    document_number = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=True)

    data = Column(Text, nullable=True)
    code = Column(Integer, nullable=True)
    code_confirmed = Column(Integer, nullable=True)
    password = Column(String(255), nullable=True)
    creator_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    photo = Column(String(255), nullable=True)
    approval_signature = Column(String(255), nullable=True)
    signature = Column(String(255), nullable=True)

    is_admin = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    is_available = Column(Boolean, default=True)

    professional_card = Column(String(255), nullable=True)
    remember_token = Column(String(25), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relaciones (opcional)
    # role = relationship("Role", backref="users", lazy="joined")
    # parent = relationship("User", remote_side=[id], backref="children", lazy="select")
    # creator = relationship("User", remote_side=[id], backref="created_users", lazy="select")
