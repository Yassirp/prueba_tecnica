from pydantic import BaseModel, Field, model_validator
from decimal import Decimal
from typing import Optional
from datetime import datetime
from modules.ParameterModule.models.m_parameters_values import MParameterValue
class MProductBase(BaseModel):
    reference: str = Field(..., max_length=255, example="P12345")
    name: str = Field(..., max_length=255, example="Product Name")
    unit_id: int = Field(..., example=1)
    value: Optional[Decimal] = Field(..., example=100.00)
    active: Optional[bool] = Field(True, example=True)

    @model_validator(mode="before")
    def validate_fields(cls, values):
        reference = values.get("reference")
        name = values.get("name")
        
        if not reference.strip():
            raise Exception("The 'reference' field cannot be empty.")
        
        if not name.strip():
            raise Exception("The 'name' field cannot be empty.")
        
        return values

    class Config:
        from_attributes = True


class MProductCreate(MProductBase):
    @model_validator(mode="before")
    def validate_foreign_keys(cls, values: dict, info):
        db = info.context.get("db", None)
        unit_id = values.get('unit_id')
        
        if unit_id:
            unit = db.query(MParameterValue).filter(MParameterValue.id == unit_id).first()
            if not unit:
                raise Exception(f"No se encontró una unidad con este id '{unit_id}'.")
            
            

class MProductUpdate(MProductBase):
    reference: Optional[str] = None
    name: Optional[str] = None
    unit_id: Optional[int] = None
    value: Optional[Decimal] = None
    active: Optional[bool] = None

    @model_validator(mode="before")
    def validate_optional_fields(cls, values):
        reference = values.get("reference")
        name = values.get("name")
        
        if reference is not None and not reference.strip():
            raise Exception("The 'reference' field cannot be empty.")
        
        if name is not None and not name.strip():
            raise Exception("The 'name' field cannot be empty.")
        
        return values


class MProductResponse(MProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
