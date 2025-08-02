
from typing import Optional
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel
from pydantic import Field

class SoccerFieldBase(BaseModel):
    name: Optional[str]
    location: Optional[str]
    capacity: Optional[int]
    price_per_hour: Optional[Decimal]
    available: Optional[bool] = True

class SoccerFieldCreate(SoccerFieldBase):
    name: str
    location: str
    capacity: int
    price_per_hour: Decimal

class SoccerFieldUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    capacity: Optional[int]
    price_per_hour: Optional[Decimal]
    available: Optional[bool]

    model_config = {
        "from_attributes": True
    }

class SoccerFieldOut(SoccerFieldBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
