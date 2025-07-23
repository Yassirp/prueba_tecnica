from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from src.app.shared.bases.base_model import BaseModel
from datetime import datetime

class Payment(BaseModel):
    __tablename__ = 'm_payments'

    id = Column(Integer, primary_key=True)
    living_group_id = Column(Integer, ForeignKey('m_living_groups.id'))
    pasarela = Column(String, nullable=True)
    payment_id = Column(String, nullable=True)
    payment_status = Column(String)
    amount = Column(Float)
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime, nullable=True)