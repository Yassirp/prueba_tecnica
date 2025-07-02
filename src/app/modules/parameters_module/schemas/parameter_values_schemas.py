from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ParameterValueBase(BaseModel):
    parameter_id: int = Field(..., description="ID del parámetro padre.")
    reference: Optional[str] = Field(default=None, description="Referencia del valor del parámetro.")
    value: Optional[str] = Field(default=None, description="Valor del parámetro.")
    description: Optional[str] = Field(default=None, description="Descripción del valor del parámetro.")
    parent_id: Optional[int] = Field(default=None, description="ID del valor padre (para jerarquías).")
    state: int = Field(default=1, description="Estado del valor (1: activo, 0: inactivo).")


class ParameterValueCreate(ParameterValueBase):
    pass


class ParameterValueUpdate(BaseModel):
    parameter_id: Optional[int] = None
    reference: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    state: Optional[int] = None


class ParameterValueOut(ParameterValueBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    # Relaciones opcionales
    children: Optional[List['ParameterValueOut']] = []
    
    model_config = {
        "from_attributes": True
    }


# Para evitar referencias circulares
ParameterValueOut.model_rebuild()
