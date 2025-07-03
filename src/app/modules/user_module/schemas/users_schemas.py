from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime
from src.app.modules.document_module.schemas.document_schemas import DocumentOut
from src.app.modules.ubication_module.schemas.country_schemas import CountryOut
from src.app.modules.ubication_module.schemas.department_schemas import DepartmentOut
from src.app.modules.ubication_module.schemas.minicipality_schemas import MunicipalityOut
from src.app.modules.permission_module.schemas.role_schema import RoleOut

class UserBase(BaseModel):
    name: str = Field(..., description="Nombre del usuario.")
    last_name: str = Field(..., description="Apellido del usuario.")
    email: EmailStr = Field(..., description="Email del usuario (debe ser único).")
    phone: str = Field(..., description="Teléfono del usuario.")
    address: str = Field(..., description="Dirección del usuario.")
    country_id: int = Field(..., description="País del usuario.")
    department_id: int = Field(..., description="Departamento del usuario.")
    municipality_id: int = Field(..., description="Municipio del usuario.")
    document_type: int = Field(..., description="Tipo de documento del usuario.")
    document_number: str = Field(..., description="Número de documento del usuario.")
    zip_code: Optional[str] = Field(default=None, description="Código postal del usuario.")
    role_id: int = Field(default=2, description="Rol del usuario.")
    created_by: Optional[int] = Field(default=None, description="ID del usuario que creó el usuario.")
    state: int = Field(default=1, description="Estado lógico del usuario.")
    code: Optional[str] = Field(default=None, description="Código de verificación del usuario.")
    campus: Optional[str] = Field(default=None, description="Campus al que pertenece el usuario.")
    time: Optional[str] = Field(default=None, description="Tiempo que lleva en LivingRoom.")
    courses: Optional[str] = Field(default=None, description="Cursos realizados por el usuario (lista separada por comas).")
    participated_in_living_group: Optional[int] = Field(default=None, description="1 si sí, 0 si no.")
    living_group_name: Optional[str] = Field(default=None, description="Nombre del grupo (si aplica).")
    did_camp: Optional[int] = Field(default=None, description="1 si sí, 0 si no.")
    data: Optional[dict] = Field(default=None, description="Datos complementarios del usuario.")

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
    created_by_user: Optional[UserBase] = None
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
