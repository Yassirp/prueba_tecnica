from datetime import datetime
from typing import Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field
from src.app.shared.bases.base_schema import BaseOutSchema

class StageBase(BaseModel):
    name: str                  = Field(max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    project_id: int            = Field(ge=1)
    description                = Field(max_length=100)

class StageCreate(StageBase):
    pass

class StageUpdate(BaseModel):
    name: Optional[str]        = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=100)
    project_id: Optional[int]  = Field(None, ge=1)
    state: Optional[int]       = Field(None, ge=0)

class StageOut(StageBase, BaseOutSchema):
    id: int = Field(ge=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
