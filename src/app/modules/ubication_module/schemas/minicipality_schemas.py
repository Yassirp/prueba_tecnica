from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime


class MunicipalityBase(BaseModel):
    department_id: int = Field(..., description="ID del departamento")
    country_code: str = Field(..., max_length=255, description="Código del país")
    department_code: str = Field(..., max_length=255, description="Código del departamento")
    code: str = Field(..., max_length=255, description="Código del municipio")
    name: str = Field(..., max_length=255, description="Nombre del municipio")

class MunicipalityCreate(MunicipalityBase):
    pass

class MunicipalityUpdate(BaseModel):
    department_id: Optional[int] = None
    country_code: Optional[str] = Field(None, max_length=255)
    department_code: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=255)
    name: Optional[str] = Field(None, max_length=255)

class MunicipalityOut(MunicipalityBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    model_config = {
        "from_attributes": True
    }