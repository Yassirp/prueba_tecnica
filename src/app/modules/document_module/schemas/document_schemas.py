from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel
from src.app.modules.parameters_module.schemas.parameter_values_schemas import ParameterValueOut

class DocumentBase(BaseModel):
    associate_id: Optional[int]
    associate_to: Optional[str]
    document_type: Optional[int]
    path: Optional[str]
    url: Optional[str]
    description: Optional[str]
    data: Optional[Any]
    created_by: Optional[int]
    active: Optional[bool] = True


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    associate_id: Optional[int]
    associate_to: Optional[str]
    document_type: Optional[int]
    path: Optional[str]
    url: Optional[str]
    description: Optional[str]
    data: Optional[Any]
    active: Optional[bool]

    class Config:
        extra = "forbid"  # Para asegurar validación estricta


class DocumentOut(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    type: Optional[ParameterValueOut]
    class Config:
        from_attributes = True