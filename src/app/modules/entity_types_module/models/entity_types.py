from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, SmallInteger, BigInteger
from sqlalchemy.orm import relationship
from ....shared.bases.base_model import Base

class EntityType(Base):
    __tablename__ = "m_entity_types"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    project_id = Column(BigInteger, ForeignKey("m_projects.id"))
    name = Column(String(100))
    description = Column(String(200), nullable=True)
    state = Column(SmallInteger)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationship with Project
    project = relationship("Project", back_populates="entity_types") 