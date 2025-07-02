from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime

class DepartmentBase(BaseModel):
    country_code: str = Field(..., max_length=255, description="Código del país")
    code: str = Field(..., max_length=255, description="Código del departamento")
    name: str = Field(..., max_length=255, description="Nombre del departamento")

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    country_code: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=255)
    name: Optional[str] = Field(None, max_length=255)

class DepartmentOut(DepartmentBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }