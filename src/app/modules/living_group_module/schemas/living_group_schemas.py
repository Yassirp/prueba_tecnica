# Archivo generado automáticamente para living_group - schemas

from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from src.app.modules.living_group_module.schemas.living_group_user_schemas import LivingGroupUserOut

if TYPE_CHECKING:
    from src.app.modules.sedes_module.schemas.sedes_schemas import SedeOut
class LivingGroupBase(BaseModel):
    name: str = Field(..., description="Nombre del grupo.")
    description: Optional[str] = Field(None, description="Descripción del grupo.")
    max_members: Optional[int] = Field(0, description="Máximo de miembros del grupo.")
    min_members: Optional[int] = Field(0, description="Mínimo de miembros del grupo.")
    start_date: Optional[datetime] = Field(None, description="Fecha de inicio del grupo.")
    start_time: Optional[str] = Field(None, description="Hora de inicio del grupo.")
    host_name: Optional[str] = Field(None, description="Nombre del anfitrión del grupo.")
    #leader_id: Optional[int] = Field(None, description="ID del líder del grupo.")
    value: Optional[float] = Field(0, description="Valor del grupo.")
    sede_id: Optional[int] = Field(None, description="ID de la sede del grupo.")
    active: Optional[bool] = Field(True, description="Estado activo del grupo.")

class LivingGroupCreate(LivingGroupBase):
    pass

class LivingGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    max_members: Optional[int] = None
    min_members: Optional[int] = None
    #leader_id: Optional[int] = None
    sede_id: Optional[int] = None
    active: Optional[bool] = None

class LivingGroupOut(LivingGroupBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    model_config = {
        "from_attributes": True
    }

class LivingGroupOutRelations(LivingGroupOut):
    getSede: Optional["SedeOut"]
    getLivingGroupUsers: Optional[List[LivingGroupUserOut]]
