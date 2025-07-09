from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class MRoleBase(BaseModel):
    code: str = Field(..., description="Código del rol")
    name: str = Field(..., description="Nombre del rol")
    active: bool = Field(..., description="Estado del rol")



class MRoleCreate(MRoleBase):
    pass


class MRoleUpdate(MRoleBase):
    code: Optional[str] = None
    name: Optional[str] = None
    active: Optional[bool] = None


class RoleOut(MRoleBase):  
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
