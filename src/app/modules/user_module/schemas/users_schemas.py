from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str = Field(..., description="Nombre del usuario.")
    last_name: str = Field(..., description="Apellido del usuario.")
    email: EmailStr
    phone: str = Field(..., description="Teléfono del usuario.")
    address: str = Field(..., description="Dirección del usuario.")
    city: int = Field(..., description="Ciudad del usuario.")
    country: int = Field(..., description="País del usuario.")
    zip_code: str = Field(..., description="Código postal del usuario.")
    role: int = Field(..., description="Rol del usuario.")
    created_by: int = Field(..., description="ID del usuario que creó el usuario.")
    state: int = Field(default=1, description="Estado lógico del usuario.")


class UserCreate(UserBase):
    password: str = Field(..., description="Contraseña del usuario.")


class UserUpdate(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[int]
    country: Optional[int]
    zip_code: Optional[str]
    role: Optional[int]
    password: Optional[str]
    state: Optional[int]


class UserOut(UserBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class ValidateLogin(BaseModel):
    email: str
    password: str


class AccessTokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"