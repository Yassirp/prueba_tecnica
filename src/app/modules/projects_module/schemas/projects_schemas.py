from pydantic import Field, BaseModel
from typing import Optional
from datetime import datetime
from ....shared.bases.base_schema import BaseOutSchema

class ProjectBase(BaseModel):
    name: str = Field(max_length=200)
    state: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectOut(ProjectBase, BaseOutSchema):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None