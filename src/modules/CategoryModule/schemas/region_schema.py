from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class RegionBase(BaseModel):
    code: str = Field(..., max_length=255, description="Código de la región")
    name: str = Field(..., max_length=255, description="Nombre de la región")
    active: Optional[bool] = Field(default=True, description="Estado activo")

    @model_validator(mode="before")
    def not_empty(cls, values):
        code = values.get('code')
        name = values.get('name')
        
        if not code.strip():
            raise Exception("El campo 'code' no puede estar vacío.")
        
        if not name.strip():
            raise Exception("El campo 'name' no puede estar vacío.")
        
        return values


class RegionCreate(RegionBase):
    pass


class RegionUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=255)
    name: Optional[str] = Field(None, max_length=255)
    active: Optional[bool]

    @model_validator(mode="before")
    def validate_optional_not_empty(cls, values):
        code = values.get('code')
        name = values.get('name')
        
        if code is not None and not code.strip():
            raise Exception("El campo 'code' no puede estar vacío si se proporciona.")
        
        if name is not None and not name.strip():
            raise Exception("El campo 'name' no puede estar vacío si se proporciona.")
        
        return values


class RegionResponse(RegionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
