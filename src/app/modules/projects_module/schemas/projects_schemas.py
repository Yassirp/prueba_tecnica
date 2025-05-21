from pydantic import Field
from typing import Optional
from datetime import datetime
from ....shared.bases.base_schema import BaseOutSchema

class ProjectBase(BaseOutSchema):
    name: str = Field(max_length=200)
    state: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None