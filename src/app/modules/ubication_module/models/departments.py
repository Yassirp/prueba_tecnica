from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql.schema import ForeignKey
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz
from sqlalchemy.orm import relationship

class Department(BaseModel):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    country_code = Column(String(10), ForeignKey("countries.code"), nullable=False)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    country = relationship("Country", back_populates="departments")
    municipalities = relationship("Municipality", back_populates="department")