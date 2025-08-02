from sqlalchemy import Column, DateTime,Integer, String, Text, Numeric, Boolean
from app.shared.bases.base_model import BaseModel
from datetime import datetime

class SoccerField(BaseModel):
    
    __tablename__ = "soccer_fields"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(Text, nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_hour = Column(Numeric(10,2), nullable=False)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
