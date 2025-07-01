from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str = Field(..., description="Nombre del usuario.")
    last_name: str = Field(..., description="Apellido del usuario.")
    email: EmailStr = Field(..., description="Email del usuario (debe ser único).")
    phone: str = Field(..., description="Teléfono del usuario.")
    address: str = Field(..., description="Dirección del usuario.")
    city_id: int = Field(..., description="Ciudad del usuario.")
    country_id: int = Field(..., description="País del usuario.")
    zip_code: Optional[str] = Field(default=None, description="Código postal del usuario.")
    role_id: int = Field(default=2, description="Rol del usuario.")
    created_by: Optional[int] = Field(default=None, description="ID del usuario que creó el usuario.")
    state: int = Field(default=1, description="Estado lógico del usuario.")
    code: Optional[str] = Field(default=None, description="Código de verificación del usuario.")

class UserCreate(UserBase):
    password: str = Field(..., description="Contraseña del usuario.")
    
    @model_validator(mode='after')
    def validate_email_unique(cls, values):
        return values


class UserUpdate(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    city_id: Optional[int]
    created_by: Optional[int]
    country_id: Optional[int]
    zip_code: Optional[str]
    role_id: Optional[int]
    password: Optional[str]
    state: Optional[int]
    
    @model_validator(mode='after')
    def validate_email_unique_update(cls, values):
        return values

class UserOutAll(UserBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]



class UserOut(UserBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }

class ValidateLogin(BaseModel):
    email: str
    password: str


class AccessTokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class CodeVerification(BaseModel):
    user_id: int
    code: str
    
class CodeVerificationOut(BaseModel):
    message: str
    code: str
    user: UserOut
    validation_method: str