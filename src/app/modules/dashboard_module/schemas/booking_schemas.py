from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class BookingBase(BaseModel):
    field_id: Optional[int] = None
    user_id: Optional[int] = None
    date: Optional[datetime] = None
    status: Optional[str] = "active"

class BookingCreate(BookingBase):
    field_id: int
    user_id: int
    date: datetime

class BookingUpdate(BaseModel):
    field_id: Optional[int] = None
    user_id: Optional[int] = None
    date: Optional[datetime] = None
    status: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class BookingOut(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    } 