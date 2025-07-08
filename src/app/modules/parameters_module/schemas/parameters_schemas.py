from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from src.app.shared.bases.base_schema import BaseOutSchema
from src.app.modules.parameters_module.schemas.parameter_values_schemas import ParameterValueOut

class ParameterBase(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    state: Optional[int]  = Field(1, ge=0)
    reference: Optional[str] = Field(None, max_length=100)

    
class ParameterCreate(ParameterBase):
    pass

class ParameterUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    state: Optional[int]  = Field(1, ge=0)
    reference: Optional[str] = Field(None, max_length=100)

class ParameterOut(ParameterBase, BaseOutSchema):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(ge=1)
    values: Optional[List[ParameterValueOut]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


