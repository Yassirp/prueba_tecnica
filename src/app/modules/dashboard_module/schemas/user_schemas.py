from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
    status: Optional[str] = "active"

class UserCreate(UserBase):
    name: str
    email: str
    role_id: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
    status: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    } 