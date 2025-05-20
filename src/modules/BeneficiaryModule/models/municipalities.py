from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Municipality(Base):
    __tablename__ = "municipalities"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    department_id = Column(BigInteger, ForeignKey("departments.id"), nullable=False)
    country_code = Column(String(255), nullable=False)
    department_code = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    department = relationship("Department", backref="municipalities")
