from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime


class MParameterBase(BaseModel):
    reference: Optional[str] = Field(None, min_length=1, max_length=100)
    value: Optional[str] = Field(None, min_length=1, max_length=255)
    active: Optional[bool] = True

    @model_validator(mode='before')
    def strip_strings(cls, values: dict) -> dict:
        for field in ('reference', 'value', 'description'):
            if field in values and isinstance(values[field], str):
                values[field] = values[field].strip()
        return values


class MParameterCreate(MParameterBase):
    pass


class MParameterUpdate(BaseModel):
    reference: Optional[str] = Field(None, min_length=1, max_length=100)
    value: Optional[str] = Field(None, min_length=1, max_length=255)
    active: Optional[bool] = None

    @model_validator(mode='before')
    def strip_strings(cls, values: dict) -> dict:
        for field in ('reference', 'value', 'description'):
            if field in values and isinstance(values[field], str):
                values[field] = values[field].strip()
        return values

class ParameterInDB(MParameterBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
