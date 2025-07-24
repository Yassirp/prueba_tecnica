from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SedesMemberBase(BaseModel):
    sede_id: int = Field(..., description="ID de la sede.")
    user_id: int = Field(..., description="ID del usuario.")
    type_id: Optional[int] = Field(None, description="Tipo de usuario en el grupo (id de parámetro)")
    description: Optional[str] = Field(None, description="Descripción del usuario en el grupo.")
    data: Optional[dict] = Field(None, description="Datos adicionales en formato JSON.")
    active: Optional[bool] = Field(True, description="Estado activo del usuario en el grupo.")

class SedesMemberCreate(SedesMemberBase):
    pass

class SedesMemberUpdate(BaseModel):
    sede_id: Optional[int] = None
    user_id: Optional[int] = None
    type_id: Optional[int] = None
    description: Optional[str] = None
    data: Optional[dict] = None
    active: Optional[bool] = None

class SedesMemberOut(SedesMemberBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    model_config = {
        "from_attributes": True
    }
