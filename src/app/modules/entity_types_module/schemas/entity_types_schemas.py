from datetime import datetime
from typing import Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field
from src.app.shared.bases.base_schema import BaseOutSchema

class EntityTypeBase(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    state: int = Field(ge=0)
    project_id: int = Field(ge=1)

class EntityTypeCreate(EntityTypeBase):
    pass

class EntityTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    state: Optional[int] = Field(None, ge=0)
    project_id: Optional[int] = Field(None, ge=1)

class EntityTypeOut(EntityTypeBase, BaseOutSchema):
    id: int = Field(ge=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None