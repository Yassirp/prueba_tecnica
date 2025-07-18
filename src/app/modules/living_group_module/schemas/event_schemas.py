from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class EventBase(BaseModel):
    name: Optional[str] = Field(None, description="Nombre del evento.")
    living_group_id: Optional[int] = Field(None, description="ID del grupo de convivencia.")
    max_members: Optional[int] = Field(0, description="Máximo de miembros del evento.")
    min_members: Optional[int] = Field(0, description="Mínimo de miembros del evento.")
    out: Optional[bool] = Field(False, description="¿Permite usuarios externos al living group?")
    start_date: Optional[datetime] = Field(None, description="Fecha de inicio del evento.")
    end_date: Optional[datetime] = Field(None, description="Fecha de fin del evento.")
    active: Optional[bool] = Field(True, description="Estado activo del evento.")

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = None
    living_group_id: Optional[int] = None
    max_members: Optional[int] = None
    min_members: Optional[int] = None
    out: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    active: Optional[bool] = None

class EventOut(EventBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    model_config = {
        "from_attributes": True
    } 