from sqlalchemy import Column, BigInteger, String, DateTime
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime
import pytz

class Country(BaseModel):
    __tablename__ = "countries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(10), unique=True, nullable=False)  # Ej: 'CO', 'US'
    name = Column(String(255), nullable=False)              # Ej: 'Colombia', 'United States'
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/Bogota')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('America/Bogota')))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
