from sqlalchemy import Column, BigInteger, String, DateTime
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Department(BaseModel):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    country_code = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
