# Archivo generado automáticamente para parameters - schemas
from datetime import datetime
from typing import Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, ConfigDict
from src.app.shared.bases.base_schema import BaseOutSchema

class ParameterBase(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    state: Optional[int]  = Field(1, ge=0)

class ParameterCreate(ParameterBase):
    pass

class ParameterUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    state: Optional[int]  = Field(1, ge=0)

class ParameterOut(ParameterBase, BaseOutSchema):
    id: int = Field(ge=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class AttributeBase(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[str]
    parameter_id: int = Field(ge=0)
    state: Optional[int] = Field(1, ge=0)

class AttributeOut(AttributeBase):
    id: int = Field(ge=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)