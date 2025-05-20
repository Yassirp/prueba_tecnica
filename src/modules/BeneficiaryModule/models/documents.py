from sqlalchemy import Column, BigInteger, Integer, String, Text, Date, TIMESTAMP
from database.base import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    associate_to = Column(String(255), nullable=False)
    associate_id = Column(BigInteger, nullable=False)
    document_type = Column(BigInteger, nullable=False)
    url = Column(String(255), nullable=False)
    description = Column(Text)
    data = Column(Text)  # 'longtext' en MySQL mapea a 'Text' en SQLAlchemy
    creator_user_id = Column(BigInteger, nullable=False)
    flow_id = Column(Integer)
    object_state_id = Column(Integer)
    user_assigned_id = Column(BigInteger)
    state = Column(Integer, default=1)
    date_resolution = Column(String(255))
    budget_value = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP, nullable=True)
