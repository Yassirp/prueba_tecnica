from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from ....shared.bases.base_schema import BaseOutSchema

class EntityTypeBase(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[str] = Field(max_length=200, nullable=True)
    state: int
    project_id: int

class EntityTypeCreate(EntityTypeBase):
    pass

class EntityTypeUpdate(EntityTypeBase):
    pass

class EntityTypeOut(EntityTypeBase, BaseOutSchema):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None