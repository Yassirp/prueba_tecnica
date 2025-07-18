# Archivo generado automáticamente para sedes - schemas

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.app.modules.parameters_module.schemas.parameter_values_schemas import ParameterValueOut

class SedeBase(BaseModel):
    name: str = Field(..., description="Nombre de la sede.")
    code: Optional[str] = Field(None, description="Código de la sede.")
    type_id: Optional[int] = Field(None, description="Tipo de sede (id de parámetro)")
    department_id: Optional[int] = Field(None, description="Departamento (id de parámetro)")
    municipality_id: Optional[int] = Field(None, description="Ciudad (id de parámetro)")
    country_id: Optional[int] = Field(None, description="País (id de parámetro)")
    address: Optional[str] = Field(None, description="Dirección de la sede.")
    phone: Optional[str] = Field(None, description="Teléfono de la sede.")
    email: Optional[str] = Field(None, description="Email de la sede.")
    website: Optional[str] = Field(None, description="Sitio web de la sede.")
    #logo: Optional[str] = Field(None, description="Logo de la sede.")
    description: Optional[str] = Field(None, description="Descripción de la sede.")
    active: Optional[bool] = Field(True, description="Estado activo de la sede.")

class SedeCreate(SedeBase):
    pass

class SedeUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    type_id: Optional[int] = None
    department_id: Optional[int] = None
    municipality_id: Optional[int] = None
    country_id: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None

class SedeOut(SedeBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    
    model_config = {
        "from_attributes": True
    }
