from ....shared.bases.base_model import Base
from sqlalchemy import Column, BigInteger, String, DateTime, SmallInteger
from datetime import datetime
from sqlalchemy.orm import relationship
class Project(Base):
    __tablename__ = "m_projects"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200))
    state = Column(SmallInteger)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    entity_types = relationship("EntityType", back_populates="project")
