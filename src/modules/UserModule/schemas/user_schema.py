from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBaseSchema(BaseModel):
    role_id: int
    document_type: int
    parent_id: Optional[int] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    document_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    data: Optional[str] = None
    code: Optional[int] = None
    code_confirmed: Optional[int] = None
    password: Optional[str] = None
    creator_user_id: int
    photo: Optional[str] = None
    approval_signature: Optional[str] = None
    signature: Optional[str] = None
    is_admin: Optional[bool] = False
    active: Optional[bool] = True
    is_available: Optional[bool] = True
    professional_card: Optional[str] = None
    remember_token: Optional[str] = None


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=6)


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)
    active: Optional[bool] = None
    is_available: Optional[bool] = None
    professional_card: Optional[str] = None
    photo: Optional[str] = None
    signature: Optional[str] = None
    approval_signature: Optional[str] = None
    remember_token: Optional[str] = None


class UserResponseSchema(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # para usar ORM mode en Pydantic v2
