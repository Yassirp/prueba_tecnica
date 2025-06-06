from datetime import datetime
from typing import Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field
from src.app.shared.bases.base_schema import BaseOutSchema

class ProjectBase(BaseModel):
    name: str = Field(max_length=100)
    state: int = Field(ge=0)
    key: str = Field(..., max_length=200, description="Clave de la empresa.")
    
class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    state: Optional[int] = Field(None, ge=0)

class ProjectOut(ProjectBase, BaseOutSchema):
    id: int = Field(ge=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
