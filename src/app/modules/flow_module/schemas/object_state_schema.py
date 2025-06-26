from pydantic import BaseModel, Field, model_validator
from typing import Optional
import re
from datetime import datetime

class ObjectStateBase(BaseModel):
    reference: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    active: Optional[bool] = True

    @model_validator(mode='before')
    def strip_strings(cls, values: dict) -> dict:
        for f in ('reference', 'name'):
            if f in values and isinstance(values[f], str):
                values[f] = values[f].strip()
        return values

    @model_validator(mode='after')
    def validate_reference_format(cls, values):
        reference = values.reference
        if not re.match(r'^[a-zA-Z0-9_]+$', reference):
            raise Exception("La referencia sólo puede contener letras, números y guiones bajos")
        return values


class ObjectStateCreate(ObjectStateBase):
    pass


class ObjectStateUpdate(BaseModel):
    reference: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    active: Optional[bool] = None

    @model_validator(mode='before')
    def strip_strings(cls, values: dict) -> dict:
        for f in ('reference', 'name'):
            if f in values and isinstance(values[f], str):
                values[f] = values[f].strip()
        return values

    @model_validator(mode='after')
    def validate_reference_format(cls, values):
        ref = values.reference
        if ref is not None and not re.match(r'^[a-zA-Z0-9_]+$', ref):
            raise Exception("La referencia sólo puede contener letras, números y guiones bajos")
        return values

class ObjectStateInDB(ObjectStateBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
