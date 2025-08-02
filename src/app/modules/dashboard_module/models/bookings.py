from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.shared.bases.base_model import BaseModel

class Booking(BaseModel):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, nullable=False)
    status = Column(String, default="active")

    user = relationship("User", backref="bookings")