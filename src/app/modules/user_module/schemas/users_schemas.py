from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime
from src.app.modules.document_module.schemas.document_schemas import DocumentOut
from src.app.modules.ubication_module.schemas.country_schemas import CountryOut
from src.app.modules.ubication_module.schemas.department_schemas import DepartmentOut
from src.app.modules.ubication_module.schemas.minicipality_schemas import MunicipalityOut
from src.app.modules.permission_module.schemas.role_schema import RoleOut
from src.app.modules.user_module.schemas.users_relationship_schemas import UserRelationshipOut
from src.app.modules.user_module.schemas.user_base_schema import UserBase

class UserCreate(UserBase):
    password: str = Field(..., description="Contraseña del usuario.")
    
    @model_validator(mode='after')
    def validate_email_unique(cls, values):
        return values


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, description="Nombre del usuario.")
    last_name: Optional[str] = Field(default=None, description="Apellido del usuario.")
    email: Optional[EmailStr] = Field(default=None, description="Email del usuario (debe ser único).")
    phone: Optional[str] = Field(default=None, description="Teléfono del usuario.")
    address: Optional[str] = Field(default=None, description="Dirección del usuario.")
    country_id: Optional[int] = Field(default=None, description="País del usuario.")
    department_id: Optional[int] = Field(default=None, description="Departamento del usuario.")
    municipality_id: Optional[int] = Field(default=None, description="Municipio del usuario.")
    document_type: Optional[int] = Field(default=None, description="Tipo de documento del usuario.")
    document_number: Optional[str] = Field(default=None, description="Número de documento del usuario.")
    created_by: Optional[int] = Field(default=None, description="ID del usuario que creó el usuario.")
    zip_code: Optional[str] = Field(default=None, description="Código postal del usuario.")
    role_id: Optional[int] = Field(default=None, description="Rol del usuario.")
    password: Optional[str] = Field(default=None, description="Contraseña del usuario.")
    state: Optional[int] = Field(default=None, description="Estado lógico del usuario.")
    is_active: Optional[bool] = Field(default=None, description="Estado activo del usuario.")

    @model_validator(mode='after')
    def validate_email_unique_update(cls, values):
        return values



class UserOut(UserBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    model_config = {
        "from_attributes": True
    }

class UserOutWithRelationships(UserBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    country: CountryOut
    department: DepartmentOut
    municipality: MunicipalityOut
    role: RoleOut
    associated_documents: list[DocumentOut]
    user_relationships: list[UserRelationshipOut]
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
