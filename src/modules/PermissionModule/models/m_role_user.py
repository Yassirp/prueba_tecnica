from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey,func
from database.base import Base

class MRoleUser(Base):
    __tablename__ = 'm_roles_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    role_id = Column(Integer, ForeignKey('m_roles.id'))
    active = Column(Boolean)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
