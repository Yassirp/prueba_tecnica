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
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    country_id: Optional[int]
    department_id: Optional[int]
    municipality_id: Optional[int]
    document_type: Optional[int]
    document_number: Optional[str]
    created_by: Optional[int]
    zip_code: Optional[str]
    role_id: Optional[int]
    password: Optional[str]
    state: Optional[int]
    
    @model_validator(mode='after')
    def validate_email_unique_update(cls, values):
        return values



class UserOut(UserBase):
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
    
    
class UserOutAll(UserBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    country: CountryOut
    department: DepartmentOut
    municipality: MunicipalityOut
    role: RoleOut
    associated_documents: list[DocumentOut]
    
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
